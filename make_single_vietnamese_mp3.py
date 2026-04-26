import json
from pathlib import Path

from google.cloud import texttospeech
from google.oauth2 import service_account


# =========================================================
# 1) Google Cloud 서비스 계정 JSON 키 붙여넣기
#    주의: 이 파일은 GitHub에 절대 올리지 말 것
# =========================================================
SERVICE_ACCOUNT_JSON = r'''
{
  "type": "service_account",
  "project_id": "acquired-badge-469703-b2",
  "private_key_id": "68f598c7670c7876db155d2a4fdbd39a4c735393",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDDVhUqDWgX3HD8\neiVaVLzJZPVHsOz3CHTrBMFrJWrdntYFSitX+cD4VG1EiDwR5+7T7mb0xdFdQ5eK\nx6moYlN9g+/7dJ2RS49ShDSVEqXNQEaa/Qgqs3MRLhNgHS0UWQYhqWUud/5lB/YN\nRRXtAzJM/xtxDXRvJvn2ImjOJMr1m/VPMfokLC4nzo4iT8fAts5g7nMKFRl+X4vu\nksupFduIBr0BCFQt2VgjxvQv0wtOlyXQUJBwrb4hj1jPrkZP4asTZ4Mop/5GqVrE\n+9O6pe2q6DR+REhB4awkHVemmueVycrYyCwYM+pzkozZgQ7SJsJk8hsltrMUnZHG\n+sUMtJ9pAgMBAAECggEAQrcSeG/mxwuH3XucaVs6tXBRY+B2NrNBN4nCw+UeOD5J\nK7pWzm/jbA1t2nPLTHRSOjkZGe28YaW1yvUBqZyXlm1rGA+Ox3Kuq0izKt0ZGt6i\nnsngMbFjkhESFggw/tue//06rSHXlcsfyw12/SHT2r9gsH6fb105D0tWT136oeK+\n7qU/9llfe9wfuZNaYjed2dQqs58ftUINGKicl7CE1a8i9Hd07q5SpTkYf4oSPV9X\nazOfD/TjL4itCuczEe8l/cnVlupUJPDfLYh2Iab/8Tzctm7mamJouQhtitqCD8ip\npWLviGS7EI+IBp6O7V07lqnxxo9F7apRUD9StOv+fwKBgQDsCdSIdfI9x1JNYCPN\nTps3mtw6vqAc16LLF7XHXLMRDxRDMdX/kjoWmHusFxCxkYNkPekwx9ZrjIz9X849\n5fnzPRpbsyLzUM3b4+nPHzqN21BASJhAtDhQeGF3g+dyobVTVr4y2mI+beyoNzNl\nixxrnWXAHnEs4kMhS6e6BmeRuwKBgQDT2w/QcM/BDEYGApQOMN8DGwZkyX6izzFW\nhMKvmp6Q605Xhpntjxn0QJuUB/aRlJJ2mhVSVxtwkKc+VDZEo66uwziDAmVVQ3Ig\nDl7oM7f74KAgUZsGQIPq+KnCKtrhkq4PjnnLRb3qP1dBzcNTE+dcBkehoQHSsw/6\no9DFPqSfKwKBgQCXB5s0TbPYj8c7tz5xSdDLfY1ZEUxF6DxEE0G+9LOnQKzIagTx\n6NC+UIchkAigdelKpMqm6ddrLZ2xKjI/LP4IA5rv/elpItT11Blw7Bx9VE0/NLQn\nAqnd44kJ/h6EHLB3SNOemlmudIuu/tMmMCLZQPcwPMpR29z0WwJRZ3OxrQKBgQCT\n+4a2YLad8EbRV+e3aee9MZlruVudugCKoL2lD+oG7HaSqNDIoZbNiHukEVPoKNGN\nyt9t3q6qGEDaRtSJaZRROsg0qu3BexUy0xb0N3wikqsHKDmTSmlbLkrV+D1gJ6cx\n8qGcnaClCY2Xx3TSiSqomzJZ8i9lz/Ivb1IbFUDEdQKBgDPPxcNM/zmD9h00svMg\nLFk9rOFXw8XolLhoeBC8dgvJPEuE+u3HlJfDo1Q5QjVShwx4XNu2t+ZuRqGLK5iY\nmXsGv6zHNMML6fWy2QE6aWWS2eu/5cTj+qSLNPCVlxMl97f5qB0PBW/C5mX1xAfL\nK2hmxVX5rQzC0lQdNFnX6HiF\n-----END PRIVATE KEY-----\n",
  "client_email": "vietnam-tts-test@acquired-badge-469703-b2.iam.gserviceaccount.com",
  "client_id": "100112837933302131256",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/vietnam-tts-test%40acquired-badge-469703-b2.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
'''


# =========================================================
# 2) 여기만 바꿔서 하나씩 생성
# =========================================================

# 생성할 베트남어 단어/문장
TEXT = "a"

# 저장할 파일 경로
# 기존 파일을 교체하려면 같은 경로로 지정
OUTPUT_MP3 = Path("audio/l0/l0-v-01.mp3")

# 최신 자연스러운 모델
VOICE_NAME = "vi-VN-Chirp3-HD-Kore"

# 다른 후보
# VOICE_NAME = "vi-VN-Chirp3-HD-Despina"
# VOICE_NAME = "vi-VN-Chirp3-HD-Erinome"
# VOICE_NAME = "vi-VN-Chirp3-HD-Gacrux"
# VOICE_NAME = "vi-VN-Chirp3-HD-Kore"
# VOICE_NAME = "vi-VN-Chirp3-HD-Laomedeia"
# VOICE_NAME = "vi-VN-Chirp3-HD-Vindemiatrix"
# VOICE_NAME = "vi-VN-Chirp3-HD-Zephyr"

# 느리게 또박또박 만들고 싶으면 Neural2 추천
# VOICE_NAME = "vi-VN-Neural2-A"
# SPEAKING_RATE = 0.85

LANGUAGE_CODE = "vi-VN"

# 이미 파일이 있어도 덮어쓸지 여부
OVERWRITE = True


def make_client() -> texttospeech.TextToSpeechClient:
    service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info
    )
    return texttospeech.TextToSpeechClient(credentials=credentials)


def make_audio_config() -> texttospeech.AudioConfig:
    # Chirp 3 HD는 최신 자연스러운 음성.
    # 속도 조절이 필요하면 Neural2로 바꾸는 것을 추천.
    if "Chirp3-HD" in VOICE_NAME:
        return texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

    # Neural2 / WaveNet / Standard용
    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.85,
        pitch=0.0,
    )


def make_single_mp3(text: str, output_path: Path) -> None:
    text = " ".join(text.strip().split())

    if not text:
        raise ValueError("TEXT가 비어 있습니다.")

    if output_path.exists() and not OVERWRITE:
        print(f"이미 파일이 있어서 생성하지 않았습니다: {output_path}")
        return

    client = make_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=LANGUAGE_CODE,
        name=VOICE_NAME,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=make_audio_config(),
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.audio_content)

    print("======================================")
    print("단일 MP3 생성 완료")
    print("======================================")
    print(f"TEXT      : {text}")
    print(f"VOICE     : {VOICE_NAME}")
    print(f"OUTPUT    : {output_path.resolve()}")
    print("======================================")


if __name__ == "__main__":
    make_single_mp3(TEXT, OUTPUT_MP3)