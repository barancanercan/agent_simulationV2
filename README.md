# 🧠 Tartışma Simülasyonu - Türkiye Siyaseti

Bu proje, Türkiye'deki siyasi tartışmaları simüle eden bir yapay zeka uygulamasıdır. CHP'li Ayşe, AKP'li Mehmet ve kararsız seçmen Miraç arasında geçen tartışmaları canlandırır.

## 🚀 Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Uygulamayı başlatın:
```bash
streamlit run app.py
```

## 🎮 Kullanım

1. Sol menüden bir gündem konusu girin
2. "Tartışmayı Başlat" butonuna tıklayın
3. Tartışmanın akışını takip edin:
   - Ayşe (CHP'li) ilk görüşünü belirtir
   - Mehmet (AKP'li) yanıt verir
   - Miraç (Hakem) soru sorar
   - Ayşe ve Mehmet Miraç'ın sorusuna yanıt verir
   - Miraç son değerlendirmesini yapar

## 🛠️ Teknolojiler

- Python 3.10+
- Streamlit
- Google Gemini API
- YAML konfigürasyon

## 📝 Notlar

- Her karakter kendi siyasi görüşüne ve kişiliğine uygun şekilde konuşur
- Tartışmalar doğal ve yerel Türkçe ile yürütülür
- Miraç, tartışmanın hakemi olarak hangi tarafın daha ikna edici olduğunu değerlendirir 