from pathlib import Path
from langchain_community.llms import LlamaCpp
import datetime



def local_llm():
    model_path = Path("models") / "Llama-3.2-3B-Instruct-Q4_K_M.gguf"

    llm = LlamaCpp(
        model_path=str(model_path),
        temperature=0.1,
        max_tokens=200,
        top_p=0.95,
        n_ctx=2048,
        n_batch=16,
        n_threads=4,  
        verbose=False
    )

    return llm

def generate_llm_response(user, current_steps, current_temp,activity):
    #print(f"generate_llm_response called with activity: {activity}")  # Debugging line
    llm = local_llm()
    

    # --- Load System Prompt ---
    system_prompt = """
    You are a helpful AI wellness assistant. 
    You give clear, friendly, and personalized advice to users based on their physical activity, health data, and environmental conditions.
    Be human-like, encouraging, and avoid technical language.
    """

    # --- Load Activity-specific Prompt ---
    if activity == "Static":
        prompt_template = open("prompts/static_prompt.txt").read()
    elif activity == "Walking":
        prompt_template = open("prompts/walk_prompt.txt").read()
    elif activity == "Running":
        prompt_template = open("prompts/run_prompt.txt").read()
    elif activity == "Climbing Stairs":
        prompt_template = open("prompts/stairs_prompt.txt").read()
    else:
        return "Unknown activity."

    print("user name ----", user.username)
    # --- Format Activity Prompt ---
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    activity_prompt = prompt_template.format(
        username= user.username,
        age=user.age,
        gender=user.gender,
        weight=user.weight,
        location=user.location,
        temperature=current_temp,
        current_time= current_time,
        daily_step_goal=user.daily_step_goal,
        current_steps = current_steps
    )

    # --- Merge with System Prompt ---
    full_prompt = system_prompt.strip() + "\n\n###\n\n" + activity_prompt.strip() + "\nBefore the messgage Always Start with Here is the response: "

    print(f"Prompt : --- \n {full_prompt}\n ----")
    response = llm(full_prompt)
    print("RESPONCEEE---",response)
    filtered_response = response.split("Here is the response:")[-1].strip()
    return filtered_response
