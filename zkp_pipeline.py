import json
import subprocess

# Путь к твоему проекту Circom в WSL
WSL_PROJECT_PATH = "/home/kali/circom_zkp_project"
WSL_INPUT_PATH = f"{WSL_PROJECT_PATH}/inputs.json"

# Абсолютные пути к node и snarkjs
NODE_PATH = "/home/kali/.nvm/versions/node/v22.15.1/bin/node"
SNARKJS_PATH = "/home/kali/.nvm/versions/node/v22.15.1/bin/snarkjs"

def save_vote_to_inputs_json(vote: int):
    if vote not in [1, 2, 3]:
        raise ValueError("Голос должен быть 1, 2 или 3")

    with open("inputs.json", "w") as f:
        json.dump({"vote": vote}, f)
    print("✅ inputs.json создан.")

def copy_inputs_to_wsl():
    subprocess.run([
        "wsl",
        "cp",
        "/mnt/c/Users/Admin/Diploma/inputs.json",
        WSL_INPUT_PATH
    ], check=True)
    print("📤 inputs.json скопирован в WSL.")

def generate_witness_in_wsl():
    cmd = (
        f"cd {WSL_PROJECT_PATH} && "
        f"{NODE_PATH} build/vote_js/generate_witness.js "
        f"build/vote_js/vote.wasm inputs.json build/witness.wtns"
    )
    subprocess.run(["wsl", "bash", "-c", cmd], check=True)
    print("🧩 witness.wtns успешно сгенерирован.")

def generate_proof_in_wsl():
    cmd = (
        f"cd {WSL_PROJECT_PATH} && "
        f"{NODE_PATH} {SNARKJS_PATH} groth16 prove "
        f"build/vote_0001.zkey build/witness.wtns proof.json public.json"
    )
    subprocess.run(["wsl", "bash", "-c", cmd], check=True)
    print("📜 Доказательство успешно сгенерировано.")

def verify_proof_in_wsl() -> bool:
    cmd = (
        f"cd {WSL_PROJECT_PATH} && "
        f"{NODE_PATH} {SNARKJS_PATH} groth16 verify "
        f"build/verification_key.json public.json proof.json"
    )
    result = subprocess.run(["wsl", "bash", "-c", cmd], capture_output=True, text=True)
    print(result.stdout)
    return "OK" in result.stdout

def run_zkp_pipeline(vote: int) -> bool:
    print("=== ZKP Pipeline запущен ===")
    save_vote_to_inputs_json(vote)
    copy_inputs_to_wsl()
    generate_witness_in_wsl()
    generate_proof_in_wsl()
    print("✅ Проверка доказательства...")
    return verify_proof_in_wsl()
