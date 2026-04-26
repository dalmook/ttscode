import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from google.cloud import texttospeech
from google.oauth2 import service_account


# =========================================================
# 1) 여기에 Google Cloud 서비스 계정 JSON 키 전체 붙여넣기
#    주의: 이 파일은 GitHub에 올리지 말 것
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
# 2) 파일/음성 설정
# =========================================================
INPUT_JSON = Path("vietnamese_a1_to_opic_im1_starter_ori.json")

# 이 파일이 최종 수정본입니다.
# 확인 후 원본 파일명으로 바꿔 GitHub에 올리면 됩니다.
OUTPUT_JSON = Path("vietnamese_a1_to_opic_im1_starter.with_audio.json")

# GitHub에 올릴 MP3 폴더
AUDIO_DIR = Path("audio")

# JSON에 들어갈 경로 prefix
# app.js에서 /audio/...를 ./audio/...로 바꿔 재생하므로 이 형태 추천
JSON_AUDIO_PREFIX = "/audio"

LANGUAGE_CODE = "vi-VN"

# 최신 모델: Chirp 3 HD
VOICE_NAME = "vi-VN-Chirp3-HD-Aoede"

# 다른 최신 모델 후보
# VOICE_NAME = "vi-VN-Chirp3-HD-Achernar"
# VOICE_NAME = "vi-VN-Chirp3-HD-Kore"
# VOICE_NAME = "vi-VN-Chirp3-HD-Charon"

# 단어장용 느린 속도가 필요하면 Neural2로 변경 가능
# VOICE_NAME = "vi-VN-Neural2-A"
# SPEAKING_RATE = 0.85

# 테스트할 때 5개만 만들고 싶으면 5로 설정
# 전체 생성하려면 None
MAX_ITEMS: Optional[int] = None

# True면 실제 MP3 생성 없이 대상/글자 수만 확인
DRY_RUN = False

# 이미 MP3 파일이 있으면 다시 생성하지 않음
SKIP_EXISTING_MP3 = True

# Google API 연속 호출 간격
SLEEP_SECONDS = 0.15


# =========================================================
# 3) Google TTS 클라이언트
# =========================================================
def make_client() -> texttospeech.TextToSpeechClient:
    service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info
    )
    return texttospeech.TextToSpeechClient(credentials=credentials)


def make_audio_config() -> texttospeech.AudioConfig:
    """
    Chirp 3 HD는 speaking_rate/pitch 조절을 지원하지 않는 경우가 있어
    최신 모델일 때는 MP3 인코딩만 지정합니다.
    """
    if "Chirp3-HD" in VOICE_NAME:
        return texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

    # Neural2/WaveNet/Standard로 바꿨을 때 사용
    return texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=0.85,
        pitch=0.0,
    )


def synthesize_mp3(
    client: texttospeech.TextToSpeechClient,
    text: str,
    output_path: Path,
) -> None:
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


# =========================================================
# 4) JSON에서 베트남어 텍스트 추출
# =========================================================
def clean_text(text: Any) -> str:
    if not isinstance(text, str):
        return ""
    return " ".join(text.strip().split())


def dialogue_text(dialogue: Dict[str, Any]) -> str:
    """
    dialogue.lines[].vi 를 하나의 MP3로 생성
    예:
    An: Xin chào!
    Min: Xin chào, bạn khoẻ không?
    """
    lines = dialogue.get("lines") or []
    parts: List[str] = []

    for line in lines:
        vi = clean_text(line.get("vi"))
        if vi:
            parts.append(vi)

    return " ".join(parts)


def audio_json_path(lesson_id: str, item_id: str) -> str:
    return f"{JSON_AUDIO_PREFIX}/{lesson_id}/{item_id}.mp3"


def audio_local_path(lesson_id: str, item_id: str) -> Path:
    return AUDIO_DIR / lesson_id / f"{item_id}.mp3"


def collect_items(data: Dict[str, Any]) -> List[Tuple[Dict[str, Any], str, str, Path, str]]:
    """
    반환값:
    [
      (json_item, text_to_speak, json_audio_path, local_mp3_path, item_type),
      ...
    ]
    """
    items = []

    for lesson in data.get("lessons", []):
        lesson_id = clean_text(lesson.get("lessonId")) or "lesson"

        # 1) 단어 카드: term만 읽기
        for card in lesson.get("vocabCards", []) or []:
            item_id = clean_text(card.get("id"))
            text = clean_text(card.get("term"))
            if item_id and text:
                items.append((
                    card,
                    text,
                    audio_json_path(lesson_id, item_id),
                    audio_local_path(lesson_id, item_id),
                    "vocab",
                ))

        # 2) 문장 카드: textVi 읽기
        for card in lesson.get("sentenceCards", []) or []:
            item_id = clean_text(card.get("id"))
            text = clean_text(card.get("textVi"))
            if item_id and text:
                items.append((
                    card,
                    text,
                    audio_json_path(lesson_id, item_id),
                    audio_local_path(lesson_id, item_id),
                    "sentence",
                ))

        # 3) 대화: lines[].vi 전체를 하나로 합쳐 읽기
        for dialogue in lesson.get("dialogues", []) or []:
            item_id = clean_text(dialogue.get("id"))
            text = dialogue_text(dialogue)
            if item_id and text:
                items.append((
                    dialogue,
                    text,
                    audio_json_path(lesson_id, item_id),
                    audio_local_path(lesson_id, item_id),
                    "dialogue",
                ))

        # 4) 발음 연습: text 읽기
        for target in lesson.get("pronunciationTargets", []) or []:
            item_id = clean_text(target.get("id"))
            text = clean_text(target.get("text"))
            if item_id and text:
                items.append((
                    target,
                    text,
                    audio_json_path(lesson_id, item_id),
                    audio_local_path(lesson_id, item_id),
                    "pronunciation",
                ))

    return items


# =========================================================
# 5) 실행
# =========================================================
def main() -> None:
    if not INPUT_JSON.exists():
        raise FileNotFoundError(f"입력 JSON 파일을 찾을 수 없습니다: {INPUT_JSON.resolve()}")

    data = json.loads(INPUT_JSON.read_text(encoding="utf-8"))
    items = collect_items(data)

    if MAX_ITEMS is not None:
        items = items[:MAX_ITEMS]

    total_chars = sum(len(text) for _, text, _, _, _ in items)

    print("======================================")
    print("Google Cloud TTS JSON MP3 생성")
    print("======================================")
    print(f"입력 JSON   : {INPUT_JSON.resolve()}")
    print(f"출력 JSON   : {OUTPUT_JSON.resolve()}")
    print(f"MP3 폴더    : {AUDIO_DIR.resolve()}")
    print(f"음성 모델   : {VOICE_NAME}")
    print(f"생성 대상   : {len(items)}개")
    print(f"총 글자 수  : {total_chars:,}자")
    print(f"DRY_RUN     : {DRY_RUN}")
    print("======================================")

    # JSON에는 먼저 audioSrc를 채워둠
    for json_item, text, json_path, local_path, item_type in items:
        json_item["audioSrc"] = json_path

    if DRY_RUN:
        OUTPUT_JSON.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print("[DRY_RUN] MP3는 생성하지 않고 JSON만 저장했습니다.")
        print(f"[DRY_RUN] 저장 JSON: {OUTPUT_JSON.resolve()}")
        return

    client = make_client()

    created = 0
    skipped = 0
    failed = 0

    for idx, (json_item, text, json_path, local_path, item_type) in enumerate(items, start=1):
        if SKIP_EXISTING_MP3 and local_path.exists():
            print(f"[{idx}/{len(items)}] SKIP 이미 있음: {local_path}")
            skipped += 1
            continue

        try:
            synthesize_mp3(client, text, local_path)
            print(f"[{idx}/{len(items)}] OK {item_type}: {local_path} | {text}")
            created += 1
            time.sleep(SLEEP_SECONDS)

        except Exception as e:
            print(f"[{idx}/{len(items)}] FAIL {item_type}: {text}")
            print(f"  -> {type(e).__name__}: {e}")
            failed += 1

    OUTPUT_JSON.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("======================================")
    print("완료")
    print("======================================")
    print(f"생성 MP3 : {created}")
    print(f"스킵 MP3 : {skipped}")
    print(f"실패     : {failed}")
    print(f"저장 JSON: {OUTPUT_JSON.resolve()}")
    print(f"MP3 폴더 : {AUDIO_DIR.resolve()}")
    print("======================================")


if __name__ == "__main__":
    main()