#The program runs here
# ONLY THE USER QUESTION GETS EMBEDDED IN REAL TIME
import sys
sys.path.append(".")

from src.pipeline import answer_question

if __name__ == "__main__":
    print("Technical Documentation Assistant (type 'exit' to quit)\n")
    while True:
        query = input("Ask a question: ")
        if query.lower() == "exit":
            break
        result = answer_question(query)
        print(f"\nAnswer:\n{result['answer']}")
        if result["sources"]:
            print(f"\nSources: {', '.join(result['sources'])}\n")
        else:
            print()