from news_summarizer import news_summarization


if __name__ == "__main__":
    url = input("Enter article URL: ")

    obj = news_summarization(url)
    obj.fetch_article()
    obj.summarization()
    obj.cleaning()

    # Save output to file
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(obj.cleaned_summary)

    print("\nSummary saved to summary.txt")
