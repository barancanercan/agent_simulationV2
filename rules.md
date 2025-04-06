# 🧠 Tartışma Simülasyonu - Türkiye Siyaseti (LLM + Streamlit)

## 🌟 Amaç

Bu yapay zeka destekli simülasyon, Türkiye'deki mevcut siyasal kutuplaşmayı temsilen iki aktif tartışmacı ajanın (CHP'li Ayşe ve AKP'li Mehmet), kullanıcıdan alınan güncel bir gündem özeti üzerinden karşılıklı olarak **birbirini ikna etmeye çalıştığı** bir etkileşimli sistem sunar.

Simülasyonda üçüncü bir ajan olan **Miraç**, kararsız/küskün bir seçmeni temsil eder ve tartışmayı analiz ederek **hangi tarafın kendisini daha çok etkilediğini** ifade eder.

Sistem, Python + Streamlit kullanılarak geliştirilecek görsel arayüz üzerinden yürütülür.

---

## 🛠️ Teknoloji ve Bileşenler

- **Gemini API 2.0**
- **Python 3.10+**
- **Streamlit** (arayüz için)
- JSON / YAML tabanlı ajan profilleri
- Gündem özetini girdi olarak alan kullanıcı modülü
- Prompt zincirleme yapısı (Multi-agent conversational flow)
- Eğer ihtiyaç duyarsan vektör database kullan. 
---

## 🏠 Tartışma Ortamları

Kullanıcı aşağıdaki ortamlardan birini seçebilir:

1. **Kahvehane**: Geleneksel Türk kahvehanesi ortamı, samimi ve rahat bir tartışma atmosferi
2. **Sokak**: Günlük hayatın içinden, doğal ve spontane bir tartışma ortamı
3. **Sokak Röportajı**: Medya tarzı, daha resmi ve yapılandırılmış bir tartışma formatı
4. **Oy Kullanılan Okulun Önü**: Seçim günü atmosferi, siyasi tartışmaların yoğun olduğu bir ortam
5. **Pazar / Market**: Günlük alışveriş ortamında geçen, doğal ve samimi tartışmalar

Her ortam, karakterlerin konuşma tarzını ve tartışmanın tonunu etkiler.

---

## 🗣️ Konuşma Kuralları

1. **Ayşe (CHP'li)**: 
   - Günlük dile uygun, 5-6 cümlelik kısa ve öz konuşmalar
   - Laiklik, liyakat ve adalet temelli argümanlar
   - Öğretici ama samimi bir ton

2. **Mehmet (AKP'li)**:
   - Günlük dile uygun, 5-6 cümlelik kısa ve öz konuşmalar
   - Hizmet ve istikrar odaklı argümanlar
   - Halk dilinde, örneklerle konuşma

3. **Miraç (Kararsız Seçmen)**:
   - Daha uzun ve detaylı konuşabilir
   - Analitik ve sorgulayıcı bir yaklaşım
   - Veriye dayalı, objektif değerlendirmeler

---

## 🧑‍💻 Sistem Prompt (LLM için Ana Yönlendirme)

```txt
Aşağıda sana üç farklı karakter tanımlanacaktır: Ayşe (CHP'li), Mehmet (AKP'li), Miraç (kararsız/küskün seçmen).  
Kullanıcı tarafından verilen gündem özeti doğrultusunda önce Ayşe ve Mehmet, sırayla doğal Türkçe ile konuşarak görüşlerini belirtir.

Her biri, siyasi kimliğine ve geçmiş deneyimlerine göre konuşur.  
Miraç ise iki tarafı dinler, ara sıra soru sorar ve tartışma sonunda kime daha yakın hissettiğini belirtir (veya hâlâ kararsız kaldığını söyler).

Tüm karakterler tutarlı, inandırıcı ve kendi perspektiflerinde kalmalıdır.

Konuşmalar kısa ama net olmalı. Her ajan kendi sesiyle yazmalı.
```

---

## 🧠 Karakter Tanımları

### 👩 Ayşe (CHP'li Tartışmacı)
- Emekli öğretmen, 62 yaşında.
- Laiklik, liyakat ve adalet temelli.
- AKP'ye karşı eleştirel.
- Kibar, öğretici ama net konuşur.

### 👨 Mehmet (AKP'li Tartışmacı)
- 52 yaşında esnaf.
- Hizmet odaklı, istikrar yanlısı.
- Erdoğan'a güven duyar.
- Samimi, halk dilinde, örneklerle konuşur.

### 👨‍💼 Miraç (Kararsız Seçmen – Hakem)
- 29 yaşında iş analisti.
- Hem CHP'ye hem AKP'ye oy vermiş, artık umutsuz.
- Veriye dayalı, analitik, sorgulayıcı.
- Kararını tartışma sonunda açıklar (veya açıkça kararsız kalır).

---

## 🔁 Akış Kuralları (Cursor-like Interaction Flow)

1. Kullanıcı gündemi girer.
2. Ayşe konuşur.
3. Mehmet yanıt verir.
4. Miraç soru sorar.
5. Ayşe cevap verir.
6. Mehmet cevap verir.
7. Miraç son değerlendirmesini yapar.

---

## 🎮 Streamlit Uygulama Özellikleri

- 📟 Gündem girişi için metin kutusu
- 🧠 Ayşe, Mehmet ve Miraç'ın konuşmalarını gösteren ayrı kutular
- ↻ Her simülasyon döngüsü için "Yeni Tartışma Başlat" butonu
- 📊 Miraç'ın görüşünü özetleyen sonuç kutusu
- Opsiyonel: İkna skoru göstergesi

---

## ✅ Örnek Kullanıcı Girdisi:

```txt
Gündem: Emeklilere yapılan zammın yetersiz olduğu ve alım gücünün düşmesi
```

---

## 🔐 Notlar

- LLM'e verilecek prompt zincirlerinde her ajanin `role`
