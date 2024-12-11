'''
失败：华尔街日报的验证反爬做的很好，需要先通过滑动验证码的检验，才能访问到真实页面。滑动验证码网上有方案，是用ui+opencv做的识别和滑动动作。
研究了检验页面的逻辑后，本想用请求方式拿到cookie然后绕过验证环节。发现有些参数不知道从哪里来的。实验失败。
收获：proxy，hooks
'''
import asyncio
import base64
import json

from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy
from pathlib2 import Path

from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from playwright.async_api import Page, BrowserContext

from urllib import parse

url = f"https://cn.wsj.com/zh-hans/news/china?mod=nav_top_section"
schema = {
    "name": "WSJ News Teaser Extractor",
    "baseSelector": "div[data-testid=tab-panel] ul li",
    "fields": [
        {"name": "title", "selector": "h4", "type": "text"},
        {"name": "link", "selector": "a[href]", "type": "attribute", "attribute": "href"},
    ],
}


async def after_goto(page: Page, context: BrowserContext):
    print("[HOOK] after_goto")
    # Example customization: log the URL
    pre_link = await page.locator('iframe').get_attribute('src')
    translated_real_request = translate_real_getcookie(pre_link)
    print()

def translate_real_getcookie(origin_url):
    print(f"origin url: {origin_url}")
    pre_url = parse.urlparse(origin_url)
    params = parse.parse_qs(pre_url.query)
    userEnv = parse.quote("574829d52b2bb14fe303c4d95ff971b768deadf98f223634a81d2569c86d0242")
    ddCaptchaChallenge = parse.quote("46297836fc404bdfb9d06c288d2d430e")
    captchaEncodedPayload = parse.quote(
        "7c9893GPlaJ2YoEfei78W6zYBAJxONQpT37BXRcioDHmI4Dyr28WOpZDliDtPBagiAiH6G-Ckg9LFSV7Gu-VmnBWnlqm8u8fBIAT03Hs3lKSw84FRE65FnjsK_8StbO0oihR4bCpJF2SKNpyNRNUIhlu1UegtKj7asrOscXvSp0fj2PDHbh99TS4ttDr-4MZU4Hjkqu2Zy-XOC4_ck_uAgDzxeIjpGSkhXZ0asKj5zgqp3RX2vPIl4Av-iJMVe4Rqq_VIislONxH2aZbocwsRQBN-VLglUAk4c3SOBsuB9Q3vKqZcsuQvL7Z-VeTrltg5A5UH84CL949NYlwoqihJq71NkBRYnWIrJTxLJPKRkMDv8wgVu5HMOV0_fcBf_MLDLTSWp8S6_dTZaGr4c7r6thbtWfw1x-VUMxhNy__QmidJ1ftvclGq8Naqx7W4BDf_BOzwsrICTdcCCxotRw1iYxaugM2sPFFFXQbekOzuWWtv6otXRvZSdH40RfJgDuvz4ap8KWgzeSDe7ShtXeo3J6n6ISEtZ2DVzBuWpakhKhkhN-VFFzQERzeGXdteX8Zk9plZ4yBXqBUimaJjGpkAMOhjd_V1ig9T7pvngbpznQgK1ZpWaqKOW_CwpQs7X8g41eZ5nVaE2c4RkK9-ThCsIRcf28ZgEF4B2uyYYgzE3Q_OS6tbGeI2MiH5D1m-5DrUHL1FJG-HAMC9BRMjnRzYihdvS9ZTmTOOpQz4E97YxthibIOSlNGQcDh243oC2Ub5Aa3LGhYDr4LOConRFjmnUrXcINMzeEH0DGyapwK8TjBKrr-vzr7InbiwnAw9Zfmob7OWx3JGv9hiDdQg5M3PGIQHwKy71Y8T0w8KyvWqspy5S9hvzypgOHlsw952orASbQcoZ9EzLlkACFWSne1RKfmHs-PdfpJGGXvxwYeem2XM2nsAhsjCHdTT-KN5uqIAP77an-lu_mRM8w46mHbjNZLkkcSCTyKPNPvafR1OymEFVBeg33dzkXPHKrruOuLJ98AxohvqBdh7DjIZc0cxTC_nnN8oK5ewKv2XhnBSGt1bQ6733JWXwjpk9sjAGxoh-1t_EWyl7UYmIB8dNt_rJc9iETL3ioT293rhrjazxPO5uN1xRWr1p2nesKTivFsSnAzcbKYOrgSOKQSUbKBaBCh_yaCXruKO7o7obPZp6-NGYCa-83fzBXya-fuPFuyVNmYKEYcY1Ywg9Dx-JDpjznSmRnBJQ_1mHJQqWbtUHmDMMf2-v_9Ov_mux03jfJKlnY0sHv8WLz-Cx-9G69dMn9e4E_v4NFMTc7iEfvg0ki2ZlxE8Su9s8KpHiSdO1XjJokZXM95wVK0UicY6sAR2QqXmiWMqEdPb0MLef3sEY_Mow6vJSFiuTXrEW20tVxJHo4lCpm9IO3zqPtpnd4F9qh8eocRAB8qo1yyrp35fVfSv5VpBX9X12yxUOT3mpwAysrSN0Y1V-TYJ12kjdzCUwDY4siuSxiAmrDCmZxH0VPNg8WhXjjssk6cPAtcijk6Z6CrlF2UMu0gtecTUj28z_oGaTT5VuNCIr19Nka68G4pnwSPdlQ0ulv2O6YewHZct2EJy0PWE1pLH5Q24paifse8byL9bv978y_2uotR5Vfn8xnqWnHURxQ7poprvJ8mIhM9Pu5qTn4z2avIMtUP-ddce84ztcZrL8YSzdZs6LDMPeDSsq1rKGKvsHC9hVBB69hOYsDpCXgPhAHXglPJLHhJAS3jz5xBIjbX5erVDIl6DMLDFxYtclLDbVj_Ai-v9czItMfsiYQR8XRyUxGwZnQXhkzUWfgAVKRvk8TV6ZTVEAZniXxnfDmFjrjm-oQBxPxEXDd92Uv5y12UZAGyoz946mfMKi27Guv1H4Vo2MsvV_HeiWhSkG_X8DRR_OUPU6KmRga5ZBURa99J_lwWRzaxyR-I12SVPlxI61uE1oCtycHVvEcfr5PIhGfQu_R7ED9BNkoFqfbP35ylkDXAIdyT94_I9PTd5i8tecDPiRUed_KCl4NojDtUZJoym-f5_oAAGGEsubbBoEujNRTWhzqiOfmdWnaPQ3p0JNz-p8P_RuRdsOa2z9XegXJcRViXLpWxRO9n9TwBTVZev59WDhw9OVhEsLTTUvgPUZ8an4LDgv3uEWophIeBgdr6RO_wbs2OV8YBUc1aSPbWIiEmZRsV5RKr4z2UeZRtHO52jmF-CpFEmOQrxICGCoCF5WhldjdfxBLsa9-MAlaSUu4WHPkHXE92PsX_VNs4YdpgTda5HeXZk84BGGAFC4mBcU-yh2Uysdx_v6frLdwExbFRQ5eN5ELq3miV-0NIKYENiqiC8fiplBsRa9PPjgExV-okXcPd_2radNqVd0WFwGW_BEJFnemg0gcs6SdJw1rJWWZIKoq5V3prHATuBRXWQGN7q_vl6KdB3_UTSKVrVXQT1ZlHirKof6htXhFfb_wua5V97EB55LT4RJLXUsXs76fFvZrf4MhKOwjy90n0oXkveO8ft_hl5qMqVyGwj8LJ6k54YO8sJh7vuSGNZm0SQN_tfbtklPb5iqovj0PUeU0JHlWgViyRul5lCkPMjEr40a10fUNLyVvUTbI2mIf8SQa4HJycioqYTkuTQ7cIhSULPUtPE2CHQc_pWfRFcjL16FQcv2hkWBxIJCVOfrOTE-7mNaVohVSYHKYq8ZrhuDla_op4hDRN0bHsg9BHvtkBb8cfCzbO_sQAW9khSk57PhVC6LRhtzQrYnRImMM5SluNFDA0L95ItRj0_6lDVW6EuDV4sbcwhAn67xCCGrAdEDpa2iUHOfTTuYGHlKG9Jd0k16XtPiB3T4q5jUFGjIvGg2sSzZIlZHHfncTqUHqdeTLqiZCINgUaQeZ65UZnMQxb6pf5rWMsJCcGPLhTEr89Ud5-VRKPGiVUYx1VcQ_YPcdI_2Jv0ZPF-cgl7fjVNvDezOPuFP366R2KgjVpKRLhkyOSYspJhnp45d0Z0ITZMxavEWcVO0zJ_zTYlUY41HPUi22TLVfrK2ImvqVjqSfsw68urHZ8pna5q9KA4KI5iJeFeJnthALNP3LHKtLvXeNzKoBrLOZ6goCM4RVC06mX-wVzEU3y1jLB0Obw7wYl6ZKo_SklVZTPeYF1qRAJVwFkFZ2fBaUOst1dZ2MKwYDTFf_Q-mctsyRVBxjkwP7I451ozO9cyx5PO4y0muVyds5I7G1g85vftU9bgu93jg431Ln_XiFV2YeDUvyEhG9gQN1zXSzmGqkstE9rrT7IT8Cpw8n3PVd8CM0DQtl2f9kgEleyPy77l6GpIIzNndRN7arBVgxYf4E8PgSt2UGn0z47Tr3zAL0I90Ug0pHZtQiJbJuviLpmv-iQecTN-LGaqkpjcxrwGrBVTBSwxN7rZnpXdty5Gm9_C1ljJbWQxBMiqupBTfNHOfaUTdZO9bEFPOE-2mCbdR7FpYvQs6h_BKgb00CptVpjoI_NxosblQFx5_sKyrowbIVBUvHW5jea-Iv2da1huUFzTkv6P7BQd-dufvyd51l614NhirrctTp_kCmvRqyGHKjqvgZzOAvyUp65riE-DL8dcTv_ZirTsSrDtWEnMIChig3F6fCliyNhElpYzZO7HhQKxQsaaY1JJ59-pzMoEn9OlfMIvbnkllCpn3NBB0ew05oHx7A4BQJ5PDyKPmf8c4XorWc8waEBBvPJUN9JAmydFCLhpu53Ud0Jidh_qGehFhYuptGW-hc0q33J74Qxtg-v8KAk9qQEHvo8O33MzjyptIJZyIS72Vfmqxin7yQiImKhLeSs7zsHEaAPyc54CNtPuZO02JEUspRaiwM2C4HRVyMWuixCpsSnEImYIVdY5ig7vj7EVcnVQntLKqGpaIu-VCdXiwXLrsmoshwsQKgjVHZDZYtoNbOZaKEEdDlkWGPmihrV5nhOTjtNHgBV306KcPilptF5BydeIDGIecVu3mZxlu9aqFDvG3QMh8-K14V1c62R6LqbtLazNRRRt6ov1lbQVXqdL-px7Np5AOY3p6HXh775fUu4GizTix-BL7pfzU-WCwYD0dz4LYuSvPBJLDvz-V_9H5XYymlrE-fZgcN5vq5CkWdwwEL5lq5MWAge_jdzHWR0PM_txd7sIcJE9bPJcULm6WibQ_l-dYuTwrrgE7oMKifZtQPK4hodZId8iz_bmkAzJtyi8yWxbfDZedvXA-VG6AQ6ljr5miP0eAmrivY1yj-kIsw-lYzr2TYYPMVIPWCURy6gcFrxDuuMZSw7lL7sSw6hDlzSQvh4ZWitK81XW1Ju5jWep7fCmRDyQT62beVXn9iwQNpnC8EgU1pWq3kQ3NgiPj8SYRxdszC9CXJKVCDXv6PEV6oEpYN7tywp95_Mqlu5MzQjLK4f9grrz2pfvDD88waztWhDVhi8sMBYhTTM8bWjbvjw0RwRieyaX1dVLmm4uMHOyw2vdr_QAEs8Il5sfJNkec4ZWn8JaWek7z4NDwBeukqkXt7jj-RHShl2wTvY69Btg8saDTn4XBRn5k4eOmBjt-WlS6dcLB7QYmHKPaoS9bDI9NUfyQMVg_TXAA-Nc0OihtCeCukGk_t9-cBVDGJEYx87soJ1hZMW9-FWrnSJlM5PwagAgn6F-V6Ek_RYVV9JHI5aNSiW3tVKSUUwYlnG-eWmryOfZHae3yx-LJHjwwVGrQqNzy3FJYNSms9GYpfa0kkRnEN1kwF-c6LIPwBR7cQqJ_c6e49w8hJo2Bv4UPr8MqkG84q_mM8fWs8Rdg7wKKinc9FbzR5dFixYGWt3g1B9Xd7wZUMR9u-e3eRjSuB8hvbFqPF5wyYVUJ_3x0afZn4dkuKdVJ7APrkrIN5Bf4B_jJijSu3h6OIqez8Mv61WZgyd5Od2sERdEzq5PwRL3l-HZoN2q6uBGu-NFPke5uHeUQocxqYFLG0IO3OVXeCIvo3yL1aUE96yFN6l2dDt7a9QAset-I2uUditLXwK6Bh5lCWyP5l72ZMm0FSjW6yJ9M1n37naCePcFJXGKPBlE6YXOcT5NKg31u1m0BBxdTL73T9EAF8A0EvXBe9rtNlhQ4TdApDbPqU6cd_h4AnbL5EsJwu7IirFsG4lb8z1spEM5fPdogOdN066iepM-GZjRXgpTTG-3XSPVj88Xv1EuIqOuUT_h2HpLrvf_jY_FQ-z-l7SUNWmaX8EVxnWE6G23yLtqayvpvtWfu4lSY6wGvhzWSOubiaoKnWnhpalHToEkZQ8SqBGpEWUdmlZZ4l-2S9h8ZIROTeo4L6IcN7smAN40r8iPkfjduR6b24zeBw5J9-IMqAWEFasNg8iFbzuU_BPN3I7iaw7LCe0Bp8osF4_9S2ongLMM8lU9GcRdZnep92MNVvjhujQ2szUZ3Ed8eYoGstEHOLJT2-WrJhdGQ28Lwl11umUqZGIcgaJONJzUo5IbpaeLD9NzXIEwdoifavyQ5rFf5zNaAWPJ-93B8618stN4cmCXzAvj_-38Uo0HUS33pc3fzEYsSXUZm_FbdlSQDJv7NmP5Cp62jELDC_9XyTy-osCOw2VKVd8cpuwSTjjpWmo1R2FLLsC8YIzkJbmvrrPqhrcNGTrz5nDWz-mOrf9wbNhp6Ez5V35H0-u06GxRNgz6HWwbaOrLGug487JF2ibV3xy2zwQ7_9WT0WHqRs6hQqpjJEvnGRmLFgPmUxnG-Eb9-Xk4zuI6ABv-RNZ5bkH5HAa4P24Q6x3nXyLnnb0nnPz_aytKEHfgUdx2qgDcQ5OQTMFFTjkdyQTNP3z3xeyHq7kW4FsCiqpqcc1ldqrBCwqDZgSuQgEZ2L0vvcDdupH89Eedab8j75KS_q0Ma9_V0Em6mZCt2SU9QS0yoia-sRkYZUxBcAyUdwz3P2GZgZFeWsRzcoVqBSDEbzq5dDHNa99zYy6b7jnvRkZWPjyC8q5RevodXEwx-X5At-vkRBZpXtWATIrQCb_mElguRnVcil0GkYDukNN8TscdBbtqhIM_monb92sIatxOGmGbf0-KAyLU2tzMvNju5QU1y3JGgX5A3GduueFIiXWeZ0pwECdLyI0b8UPs3rWv5KSMn4ylq23-rq-f075vCuOD3IC6LxFjMOHi48GkmtaVdbEm42dEmK8p9Dw8D2EU3maq7loDb4rBS1z68dsyjQebMVfwQlQsoUU68JafgsALTp7ffLZn0bajtz-Pd15ut9PzMdQFf7DkMLOrkzhvAxg_Pdc9Kex84iYRKKKPxqMZjIoIZW8WUqUuDIGRXNjEu60OHD4ma3kDxFC-ATK4HF57BZxRZ6YUdt7Dx4alftnmc3r8kyVp1gtDhuDNczywLuryrVkg5Exad5Iwqcv_G7WOZWmBa6akWzHxxNELS3hp3bo88aZd6UoDL5ptBRqQaBuX5jvlE6kKZmaa_DphQLukNX")
    ddCaptchaEnv = parse.quote(
        "db5814b294fcb2271d9cddd3fca9061a67f94541414bb8689750eb2601e2195c637185a0d63310b09b6a6178eaed575699de4c2867412d6a3458e0c64f2a015840125b093b8dcd9161eb855bb865c447")
    ddCaptchaAudioChallenge = parse.quote("d5c231252b117877d0cb80aa8927109a")
    ua = parse.quote(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    real_request_query = f"cid={parse.quote(params['cid'][0])}&icid={parse.quote(params['initialCid'][0])}&ccid=&userEnv={userEnv}&dm={parse.quote(params['dm'][0])}&ddCaptchaChallenge={ddCaptchaChallenge}&ddCaptchaEncodedPayload={captchaEncodedPayload}&ddCaptchaEnv={ddCaptchaEnv}&ddCaptchaAudioChallenge={ddCaptchaAudioChallenge}&hash={parse.quote(params['hash'][0])}&ua={ua}&referer={parse.quote(params['referer'][0])}&parent_url={parse.quote(origin_url)}&x-forwarded-for=&s={parse.quote(params['s'][0])}&ir="
    print(f"encoded: {real_request_query}")

async def on_execution_started(page: Page, context: BrowserContext):
    print("[HOOK] on_execution_started")
    # Example customization: perform actions after JS execution
    await page.evaluate("console.log('Custom JS executed')")


# https://github.com/unclecode/crawl4ai
async def extract_items(input):
    screenshot_file = Path(f"../../screenshots/{Path(__file__).stem}.png")

    crawler_strategy = AsyncPlaywrightCrawlerStrategy(verbose=True)
    crawler_strategy.set_hook('after_goto', after_goto)
    crawler_strategy.set_hook('on_execution_started', on_execution_started)

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    async with AsyncWebCrawler(
            verbose=True,
            headless=False,
            # crawler_strategy=crawler_strategy, # 这种传递方式不行，用了下面的set_hook
            proxy="socks5://127.0.0.1:10808",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ) as crawler:
        crawler.crawler_strategy.set_hook('after_goto', after_goto)
        crawler.crawler_strategy.set_hook('on_execution_started', on_execution_started)
        result = await crawler.arun(
            url=url,
            extraction_strategy=extraction_strategy,
            cache_mode=CacheMode.BYPASS,
            wait_for="css:#nav",
            screenshot=True,
            screenshot_wait_for=5.0,  # Wait 2 seconds before capture
            magic=True,  # Enables all anti-detection features
        )
        assert result.success, "无法爬取该页面"

        with open(screenshot_file, mode="wb+") as f:
            f.write(base64.b64decode(result.screenshot))
            print(f"把截图保存到{screenshot_file}")
        # Soone will be change to result.markdown
        # print(result.markdown_v2.raw_markdown)
        news_teasers = json.loads(result.extracted_content)
        print(f"成功提取了 {len(news_teasers)} 条")
        print(json.dumps(news_teasers, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(extract_items(input))
