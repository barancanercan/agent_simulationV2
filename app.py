import streamlit as st
import google.generativeai as genai
import yaml
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Tartışma ortamları
DISCUSSION_ENVIRONMENTS = {
    "Kahvehane": "Geleneksel Türk kahvehanesi ortamı, samimi ve rahat bir tartışma atmosferi",
    "Sokak": "Günlük hayatın içinden, doğal ve spontane bir tartışma ortamı",
    "Sokak Röportajı": "Medya tarzı, daha resmi ve yapılandırılmış bir tartışma formatı",
    "Oy Kullanılan Okulun Önü": "Seçim günü atmosferi, siyasi tartışmaların yoğun olduğu bir ortam",
    "Pazar / Market": "Günlük alışveriş ortamında geçen, doğal ve samimi tartışmalar"
}

# Load agent configurations
def load_agents():
    try:
        with open('config/agents.yaml', 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)['agents']
    except FileNotFoundError:
        st.error("agents.yaml dosyası bulunamadı. Lütfen config klasörünü kontrol edin.")
        return None

# Initialize session state
if 'discussion_history' not in st.session_state:
    st.session_state.discussion_history = []
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'current_environment' not in st.session_state:
    st.session_state.current_environment = "Kahvehane"
if 'current_speaker' not in st.session_state:
    st.session_state.current_speaker = None
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'waiting_for_user' not in st.session_state:
    st.session_state.waiting_for_user = False
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'discussion_summary' not in st.session_state:
    st.session_state.discussion_summary = ""
if 'discussion_complete' not in st.session_state:
    st.session_state.discussion_complete = False
if 'next_step' not in st.session_state:
    st.session_state.next_step = 0
if 'waiting_for_mirac' not in st.session_state:
    st.session_state.waiting_for_mirac = False
if 'current_speaker_index' not in st.session_state:
    st.session_state.current_speaker_index = 0  # 0: Ayşe, 1: Mehmet
if 'conversation_round' not in st.session_state:
    st.session_state.conversation_round = 0  # Kaç tur konuşulduğunu takip etmek için
if 'continuous_conversation' not in st.session_state:
    st.session_state.continuous_conversation = True  # Sürekli konuşma modu
if 'api_error' not in st.session_state:
    st.session_state.api_error = False  # API hatası durumunu takip etmek için
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0  # Son istek zamanını takip etmek için

def get_agent_response(agent, topic, history, environment):
    agents = load_agents()
    agent_config = agents[agent]
    
    # Tarihsel olayları string'e çevir
    historical_events = "\n".join([f"- {event}" for event in agent_config['historical_events']])
    
    # Konuşma uzunluğu ayarı
    length_instruction = ""
    if agent in ['ayse', 'mehmet']:
        length_instruction = "Cevabın 5-6 cümlelik kısa ve öz olmalı, günlük dile uygun olmalı."
    else:  # Miraç için
        length_instruction = "Cevabın daha detaylı ve analitik olabilir, veriye dayalı değerlendirmeler yapabilirsin."
    
    # AKP'li Mehmet için özel prompt
    if agent == 'mehmet':
        prompt = f"""
        Sen {agent_config['name']} adında bir {agent_config['role']}sın.
        Yaşın: {agent_config['age']}
        Geçmişin: {agent_config['background']}
        Özelliklerin: {', '.join(agent_config['traits'])}
        Konuşma tarzın: {agent_config['speaking_style']}

        Şu an {environment} ortamında tartışma yapıyorsunuz.
        Ortamın özellikleri: {DISCUSSION_ENVIRONMENTS[environment]}

        Tarihsel deneyimlerin ve bu olaylardan nasıl etkilendiğin:
        {historical_events}

        Gündem konusu: {topic}

        Önceki konuşmalar:
        {history}

        {length_instruction}
        Konuşman doğal ve yerel Türkçe ile olmalı, politik ezber cümlelerden kaçınmalısın.
        Halk dilinde, samimi ve örneklerle konuş.
        """
    else:
        prompt = f"""
        Sen {agent_config['name']} adında bir {agent_config['role']}sın.
        Yaşın: {agent_config['age']}
        Geçmişin: {agent_config['background']}
        Özelliklerin: {', '.join(agent_config['traits'])}
        Konuşma tarzın: {agent_config['speaking_style']}

        Şu an {environment} ortamında tartışma yapıyorsunuz.
        Ortamın özellikleri: {DISCUSSION_ENVIRONMENTS[environment]}

        Tarihsel deneyimlerin ve bu olaylardan nasıl etkilendiğin:
        {historical_events}

        Gündem konusu: {topic}

        Önceki konuşmalar:
        {history}

        {length_instruction}
        Konuşman doğal ve yerel Türkçe ile olmalı, politik ezber cümlelerden kaçınmalısın.
        """
    
    # Gemini 2.0 modelini kullan
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    # Yükleme durumunu göster
    st.session_state.is_loading = True
    
    # API istekleri arasında 5 saniye bekle
    current_time = time.time()
    time_since_last_request = current_time - st.session_state.last_request_time
    if time_since_last_request < 5:
        time.sleep(5 - time_since_last_request)
    
    try:
        response = model.generate_content(prompt)
        st.session_state.last_request_time = time.time()
        st.session_state.api_error = False
        return response.text
    except Exception as e:
        st.session_state.api_error = True
        st.error(f"Model hatası: {str(e)}")
        # Hata durumunda basit bir yanıt döndür
        if agent == 'ayse':
            return "Bu durum gerçekten üzücü. Laiklik ve adalet ilkelerimizden vazgeçmemeliyiz."
        elif agent == 'mehmet':
            return "Devletimiz her zaman doğru olanı yapar. Güveniyoruz ve destekliyoruz."
        else:
            return "Bu konuda daha fazla bilgiye ihtiyacım var. Her iki tarafın da argümanlarını değerlendirmeliyim."
    finally:
        st.session_state.is_loading = False

def summarize_discussion(topic, history):
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    prompt = f"""
    Sen bir siyasi tartışma analisti olarak görev yapıyorsun.
    
    Gündem konusu: {topic}
    
    Tartışma geçmişi:
    {history}
    
    Lütfen bu tartışmayı özetle. Şu noktalara değin:
    1. Her iki tarafın ana argümanları neler?
    2. Hangi tarihsel olaylar tartışmada gündeme geldi?
    3. Tartışmanın genel tonu nasıl?
    4. Hangi konularda uzlaşma var, hangi konularda çatışma var?
    
    Özeti 3-4 paragraf halinde, objektif bir şekilde yaz.
    """
    
    # API istekleri arasında 5 saniye bekle
    current_time = time.time()
    time_since_last_request = current_time - st.session_state.last_request_time
    if time_since_last_request < 5:
        time.sleep(5 - time_since_last_request)
    
    try:
        response = model.generate_content(prompt)
        st.session_state.last_request_time = time.time()
        st.session_state.api_error = False
        return response.text
    except Exception as e:
        st.session_state.api_error = True
        st.error(f"Özet oluşturma hatası: {str(e)}")
        return "Tartışma özeti oluşturulamadı."

def start_new_discussion():
    st.session_state.discussion_history = []
    st.session_state.current_topic = ""
    st.session_state.current_speaker = None
    st.session_state.is_loading = False
    st.session_state.waiting_for_user = False
    st.session_state.user_input = ""
    st.session_state.discussion_summary = ""
    st.session_state.discussion_complete = False
    st.session_state.next_step = 0
    st.session_state.waiting_for_mirac = False
    st.session_state.current_speaker_index = 0  # 0: Ayşe, 1: Mehmet
    st.session_state.conversation_round = 0  # Kaç tur konuşulduğunu takip etmek için
    st.session_state.continuous_conversation = True  # Sürekli konuşma modu
    st.session_state.api_error = False
    st.session_state.last_request_time = 0

# Streamlit UI
st.title("🧠 Tartışma Simülasyonu - Türkiye Siyaseti")

# Sidebar for new discussion
with st.sidebar:
    st.header("Yeni Tartışma")
    
    # Tartışma ortamı seçimi
    st.subheader("Tartışma Ortamı")
    selected_environment = st.selectbox(
        "Ortam seçin:",
        options=list(DISCUSSION_ENVIRONMENTS.keys()),
        index=list(DISCUSSION_ENVIRONMENTS.keys()).index(st.session_state.current_environment)
    )
    st.session_state.current_environment = selected_environment
    st.caption(DISCUSSION_ENVIRONMENTS[selected_environment])
    
    # Gündem konusu girişi
    new_topic = st.text_area("Gündem Konusu:", 
                            placeholder="Örnek: Emeklilere yapılan zamın yetersiz olduğu ve alım gücünün düşmesi")
    
    if st.button("Tartışmayı Başlat"):
        if new_topic:
            start_new_discussion()
            st.session_state.current_topic = new_topic
        else:
            st.warning("Lütfen bir gündem konusu girin!")
    
    # Tarafsız Seçmen Yorumu butonu
    if st.session_state.current_topic and st.session_state.continuous_conversation:
        st.divider()
        st.subheader("Tarafsız Seçmen Yorumu")
        if st.button("Tarafsız Seçmen Yorumu", key="mirac_button"):
            st.session_state.continuous_conversation = False
            st.session_state.next_step = 3  # Miraç'ın konuşmasına geç
            st.rerun()

# Main content area
if st.session_state.current_topic:
    st.subheader(f"Gündem: {st.session_state.current_topic}")
    st.caption(f"Ortam: {st.session_state.current_environment}")
    
    # API hatası uyarısı
    if st.session_state.api_error:
        st.warning("API kotası aşımı nedeniyle basit yanıtlar kullanılıyor. Lütfen daha sonra tekrar deneyin.")
    
    # Discussion flow
    if st.session_state.next_step == 0:
        # Ayşe's first response
        st.session_state.current_speaker = "Ayşe"
        ayse_response = get_agent_response('ayse', st.session_state.current_topic, "", st.session_state.current_environment)
        st.session_state.discussion_history.append(("Ayşe", ayse_response))
        st.session_state.next_step = 1
        st.rerun()
        
    elif st.session_state.next_step == 1:
        # Mehmet's response
        st.session_state.current_speaker = "Mehmet"
        mehmet_response = get_agent_response('mehmet', st.session_state.current_topic, 
                                           "\n".join([f"{name}: {text}" for name, text in st.session_state.discussion_history]),
                                           st.session_state.current_environment)
        st.session_state.discussion_history.append(("Mehmet", mehmet_response))
        
        # Sürekli konuşma modunda ise tekrar Ayşe'ye dön
        if st.session_state.continuous_conversation:
            st.session_state.next_step = 0
            st.rerun()
        else:
            st.session_state.next_step = 2
            st.rerun()
            
    elif st.session_state.next_step == 2:
        # Kullanıcıya Miraç için buton göster
        st.info("Tartışmayı değerlendirmek için sol menüden 'Tarafsız Seçmen Yorumu' butonuna tıklayın.")
            
    elif st.session_state.next_step == 3:
        # Miraç's question
        st.session_state.current_speaker = "Miraç"
        mirac_question = get_agent_response('mirac', st.session_state.current_topic,
                                          "\n".join([f"{name}: {text}" for name, text in st.session_state.discussion_history]),
                                          st.session_state.current_environment)
        st.session_state.discussion_history.append(("Miraç", mirac_question))
        st.session_state.next_step = 4
        st.rerun()
        
    elif st.session_state.next_step == 4:
        # Ayşe's answer to Miraç
        st.session_state.current_speaker = "Ayşe"
        ayse_response = get_agent_response('ayse', st.session_state.current_topic,
                                         "\n".join([f"{name}: {text}" for name, text in st.session_state.discussion_history]),
                                         st.session_state.current_environment)
        st.session_state.discussion_history.append(("Ayşe", ayse_response))
        st.session_state.next_step = 5
        st.rerun()
        
    elif st.session_state.next_step == 5:
        # Mehmet's answer to Miraç
        st.session_state.current_speaker = "Mehmet"
        mehmet_response = get_agent_response('mehmet', st.session_state.current_topic,
                                           "\n".join([f"{name}: {text}" for name, text in st.session_state.discussion_history]),
                                           st.session_state.current_environment)
        st.session_state.discussion_history.append(("Mehmet", mehmet_response))
        st.session_state.next_step = 6
        st.rerun()
        
    elif st.session_state.next_step == 6:
        # Kullanıcıya Miraç'ın son değerlendirmesi için buton göster
        st.info("Tartışmanın son değerlendirmesi için sol menüden 'Tarafsız Seçmen Yorumu' butonuna tıklayın.")
        if st.button("Tarafsız Seçmen Yorumu", key="mirac_2"):
            st.session_state.next_step = 7
            st.rerun()
            
    elif st.session_state.next_step == 7:
        # Miraç's final evaluation
        st.session_state.current_speaker = "Miraç"
        mirac_evaluation = get_agent_response('mirac', st.session_state.current_topic,
                                            "\n".join([f"{name}: {text}" for name, text in st.session_state.discussion_history]),
                                            st.session_state.current_environment)
        st.session_state.discussion_history.append(("Miraç", mirac_evaluation))
        
        # Tartışma özeti oluştur
        st.session_state.discussion_summary = summarize_discussion(
            st.session_state.current_topic,
            "\n".join([f"{name}: {text}" for name, text in st.session_state.discussion_history])
        )
        
        st.success("Tartışma tamamlandı!")
        st.session_state.discussion_complete = True
        st.session_state.next_step = 8

    # Display discussion history in chat-like format
    for name, text in st.session_state.discussion_history:
        with st.container():
            if name == "Ayşe":
                st.markdown(f"**👩 {name} (CHP'li):** {text}")
            elif name == "Mehmet":
                st.markdown(f"**👨 {name} (AKP'li):** {text}")
            else:
                st.markdown(f"**👨‍💼 {name} (Hakem):** {text}")
            st.divider()
    
    # Tartışma özeti
    if st.session_state.discussion_summary:
        st.subheader("Tartışma Özeti")
        st.markdown(st.session_state.discussion_summary)

else:
    st.info("Lütfen sol menüden bir gündem konusu girerek tartışmayı başlatın.") 