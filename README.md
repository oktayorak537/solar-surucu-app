# Ortec Solar Sürücü Hesaplama Modülü

Bu proje Streamlit ile yapılmış basit bir hesaplama aracıdır. Telefonda veya bilgisayarda tarayıcı üzerinden çalışır.

## Dosyalar
- `app.py` — Uygulama kodu
- `requirements.txt` — Bağımlılıklar
- `logo.png` — (opsiyonel) Logonuzu bu isimle `app.py` ile aynı klasöre koyun

## Yerelde Çalıştırma
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Streamlit Community Cloud'a Yükleme (bilgisayar kapalıyken de çalışır)
1. GitHub'da bir repo açın (örn. `ortec-solar-app`).
2. `app.py`, `requirements.txt` ve opsiyonel `logo.png` dosyalarını yükleyin.
3. https://share.streamlit.io üzerinden **Deploy an app** deyin, reponuzu seçin.
4. Branch: `main`, dosya: `app.py` → Deploy.
5. Size herkese açık bir URL verecek: `https://<app-adiniz>-<kullanici>.streamlit.app`

## Hugging Face Spaces Alternatifi
1. https://huggingface.co/spaces → **Create new Space** → **Streamlit**.
2. Dosyaları ekleyin ve Space'i başlatın.
3. Size bir public URL verir.
