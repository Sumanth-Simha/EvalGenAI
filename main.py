# main.py

from agent.router import route


def show_intro():
    print("\n🔥 EvalGenAI - AI Academic Assistant")
    print("=" * 60)
    print("Type 'exit' to quit\n")

    print("💡 Try queries like:")
    print(" - Explain IoT framework")
    print(" - Explain OSI model with diagram")
    print(" - Predict important questions from IoT")
    print("=" * 60)


def main():
    show_intro()

    while True:
        try:
            query = input("\nAsk: ").strip()

            if not query:
                print("⚠️ Please enter a valid query.")
                continue

            if query.lower() == "exit":
                print("\n👋 Exiting EvalGenAI. Good luck with your exams!")
                break

            result = route(query)

            print("\n" + "=" * 60)
            print("🔥 OUTPUT")
            print("=" * 60)
            print(result)
            print("=" * 60)

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Exiting...")
            break

        except Exception as e:
            print("\n⚠️ Unexpected error occurred:", e)
            print("👉 Try again.\n")


if __name__ == "__main__":
    main()