"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str) -> str:
    client = genai.Client(api_key=get_api_key())

    start_time = time.perf_counter()
    response = client.models.generate_content(model=MODEL, contents=question)
    elapsed_seconds = time.perf_counter() - start_time

    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else None
    output_tokens = usage.candidates_token_count if usage else None

    print(
        f"\n[トークン数] 入力: {input_tokens if input_tokens is not None else '不明'}, "
        f"出力: {output_tokens if output_tokens is not None else '不明'}"
        f"\n[回答時間] {elapsed_seconds:.2f}秒\n"
    )

    # ここまで

    return response.text

def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        print(ask(args.question))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)

"""
def ask(chat, question: str) -> str:
    response = chat.send_message(question)

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage else None
    output_tokens = usage.candidates_token_count if usage else None

    print(
        f"\n[トークン数] 入力: {input_tokens if input_tokens is not None else '不明'}, "
        f"出力: {output_tokens if output_tokens is not None else '不明'}\n"
    )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="会話履歴を保ってLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    question = args.question

    while True:
        print(f"[質問] {question}\n")
        try:
            print(ask(chat, question))
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))

        question = input("\n次の質問（終了するには exit）> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
"""
            
if __name__ == "__main__":
    main()
