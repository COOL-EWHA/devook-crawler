from key_phrase_with_crawler.lambda_function_for_test import lambda_handler


def get_test_document():
    content = lambda_handler(
        {
             "url": "https://jojoldu.tistory.com/603"
        },
        None,
    )

    # 기능 : 크롤링한 데이터를 5120 만큼씩 잘라서 list에 저장하기
    test_document = []
    for i in range(0, len(content), 5120):
        if len(content) > 5120:
            print("Seperated Content size : %d" % len(content[i:i + 5120]))
            test_document.append(content[i:i + 5119])
        else:
            print("Seperated Content size : %d" % len(content[i:]))
            test_document.append(content[i:])

    return test_document
