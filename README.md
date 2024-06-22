# BE_youtube-data

### Youtube 영상 다운로드 오픈소스
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---
### 셀레니움 코드 동작을 위해서는 크롬드라이버가 설치되어 있어야 합니다.
- [Window](https://spectrum20.tistory.com/entry/python-Selenium-%ED%81%AC%EB%A1%AC-%EB%B8%8C%EB%9D%BC%EC%9A%B0%EC%A0%80) 
- [Mac](https://ddingmin00.tistory.com/entry/mac-m1-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-Selenium-Chromedriver-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0)

---

## YouTube 데이터 추출 스크립트 사용 설명서

이 스크립트는 YouTube 비디오에서 다양한 정보를 추출하는 데 사용됩니다. 아래는 사용 가능한 명령행 인자들과 예시들입니다.

### 명령행 인자 설명

#### 필수 인자:

- `--channel_id` \<channel_id\>: 추출할 YouTube 채널의 ID입니다.
- `--cpus` \<num_cpus\>: 사용할 CPU 코어 수입니다.

#### 선택적 인자:

- `--folder` \<folder_path\>: 추출된 데이터를 저장할 폴더 경로입니다.

#### 옵션 인자:

- `--viewing`: YouTube 비디오의 시청 분포를 HTML로 파싱합니다.
- `--chat`: YouTube 비디오의 실시간 채팅을 추출합니다.
- `--sound`: YouTube 비디오의 오디오를 추출합니다.
- `--all`: 모든 기능을 실행합니다. (기본값)

### 예시

#### 기본 사용:

다음 예시는 모든 기능을 사용하여 YouTube 비디오에서 데이터를 추출하는 방법을 보여줍니다.

```bash
python your_script.py --channel_id ABCDEFGHIJ --cpus 4 --folder /path/to/save/folder
```

#### 개별 기능 실행:

특정 기능만 실행하려면 해당 옵션을 사용합니다.

- **HTML 파싱만 실행:**

  ```bash
  python your_script.py --channel_id ABCDEFGHIJ --cpus 4 --folder /path/to/save/folder --viewing
  ```

- **실시간 채팅 추출만 실행:**

  ```bash
  python your_script.py --channel_id ABCDEFGHIJ --cpus 4 --folder /path/to/save/folder --chat
  ```

- **오디오 추출만 실행:**

  ```bash
  python your_script.py --channel_id ABCDEFGHIJ --cpus 4 --folder /path/to/save/folder --sound
  ```

#### 선택적 옵션 활용:

특정 옵션을 선택하여 실행할 수 있습니다.

- **특정 옵션만 실행:**

  예를 들어, 시청 분포 파싱과 실시간 채팅 추출만 실행하려면 다음과 같이 입력합니다.

  ```bash
  python your_script.py --channel_id ABCDEFGHIJ --cpus 4 --folder /path/to/save/folder --viewing --chat
  ```

### 상세 정보

- `--channel_id`: 추출할 YouTube 채널의 ID를 지정합니다. 이는 필수 인자입니다.
- `--cpus`: 사용할 CPU 코어의 수를 지정합니다. 이는 병렬 처리에 사용됩니다.
- `--folder`: 추출된 데이터를 저장할 폴더의 경로를 지정합니다. 이 값이 주어지지 않으면 기본 폴더에 저장됩니다.

- `--viewing`: YouTube 비디오의 시청 분포를 HTML로 파싱하여 데이터를 추출합니다.
- `--chat`: YouTube 비디오의 실시간 채팅을 추출합니다.
- `--sound`: YouTube 비디오의 오디오를 추출합니다.
- `--all`: 모든 기능을 실행합니다. 이는 기본적으로 설정되어 있으며 다른 기능 옵션이 지정되지 않은 경우 실행됩니다.

### 주의 사항

- 본 스크립트는 Ray를 사용하여 병렬 처리를 구현합니다. 따라서 `--cpus` 옵션에 지정한 수만큼의 CPU 코어가 필요합니다.
- 데이터 추출 도중 오류가 발생할 경우 오류 처리가 자동으로 이루어집니다.

---