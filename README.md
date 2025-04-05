# 🧠 Türkiye Siyaseti Tartışma Simülasyonu

## 🌟 Proje Hakkında

Bu proje, Türkiye'deki siyasi tartışmaları simüle eden yapay zeka destekli bir uygulamadır. İki farklı siyasi görüşü temsil eden karakterler (CHP'li Ayşe ve AKP'li Mehmet) ve bir kararsız seçmen (Miraç) arasında geçen tartışmaları canlandırır.

## 🛠️ Teknolojiler

- Python 3.10+
- Streamlit
- Google Gemini API
- YAML/JSON
- dotenv

## 🏠 Tartışma Ortamları

Uygulama, farklı tartışma ortamları sunar:

1. **Kahvehane**: Geleneksel Türk kahvehanesi ortamı
2. **Sokak**: Günlük hayatın içinden tartışmalar
3. **Sokak Röportajı**: Medya tarzı tartışmalar
4. **Oy Kullanılan Okulun Önü**: Seçim günü atmosferi
5. **Pazar / Market**: Günlük alışveriş ortamında tartışmalar

## 👥 Karakterler

### Ayşe (CHP'li)
- Emekli öğretmen, 62 yaşında
- Laiklik ve liyakat temelli argümanlar
- Öğretici ve net bir konuşma tarzı

### Mehmet (AKP'li)
- 52 yaşında esnaf
- Hizmet ve istikrar odaklı
- Halk dilinde, örneklerle konuşma

### Miraç (Kararsız Seçmen)
- 29 yaşında iş analisti
- Veriye dayalı değerlendirmeler
- Analitik ve sorgulayıcı yaklaşım

## 🚀 Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/barancanercan/agent_simulationV2.git
cd agent_simulationV2
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyasını oluşturun:
```
GOOGLE_API_KEY=your_api_key_here
```

4. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

## 📝 Kullanım

1. Sol menüden tartışma ortamını seçin
2. Gündem konusunu girin
3. "Tartışmayı Başlat" butonuna tıklayın
4. Karakterlerin tartışmasını takip edin
5. "Tarafsız Seçmen Yorumu" butonu ile Miraç'ın değerlendirmesini görün

## 🤝 Katkıda Bulunma

1. Fork'layın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'feat: Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📞 İletişim

Baran Can Ercan - [@barancanercan](https://github.com/barancanercan)

Proje Linki: [https://github.com/barancanercan/agent_simulationV2](https://github.com/barancanercan/agent_simulationV2) 