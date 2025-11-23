def start_quiz(cate):
    score = 0
    total_questions = len(cate)
    print("\n--- Quiz Starting ---")

    for q in cate:
        print("\n" + q["question"])
        for i, option in enumerate(q["options"]):
            print(f"  {i + 1}. {option}")

        user_choice = input("Your answer (1-4): ")

        user_answer_text = ""
        # Safely get the answer text based on index
        if user_choice in ["1", "2", "3", "4"]:
            user_answer_text = q["options"][int(user_choice) - 1]

        if user_answer_text == q["answer"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. The correct answer was: {q['answer']}")

    print("\n--- Quiz Finished ---")
    print(f"Your final score is: {score} out of {total_questions}")
    return score