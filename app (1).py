
st.title("🔍 Comparador Facial – Face++ API")

# Pegando as keys do secrets corretamente
API_KEY = "C70B3cOgSZaxCy1BlKbsvQIuJLe_zhYU"
API_SECRET = "qMltGsxAXZU8AlL1ZJobDSMerpCZ1ObT"


COMPARE_URL = "https://api-us.faceplusplus.com/facepp/v3/compare"

st.write("Envie duas imagens para verificar se são da mesma pessoa.")

# Upload das imagens
col1, col2 = st.columns(2)

with col1:
    img1_file = st.file_uploader("Imagem 1", type=["jpg", "jpeg", "png"], key="img1")
    if img1_file:
        st.image(img1_file, caption="Imagem 1", use_column_width=True)

with col2:
    img2_file = st.file_uploader("Imagem 2", type=["jpg", "jpeg", "png"], key="img2")
    if img2_file:
        st.image(img2_file, caption="Imagem 2", use_column_width=True)

# Comparar
if st.button("Comparar Faces"):
    if not img1_file or not img2_file:
        st.error("Envie as duas imagens!")
        st.stop()

    img1_bytes = img1_file.read()
    img2_bytes = img2_file.read()

    files = {
        "image_file1": img1_bytes,
        "image_file2": img2_bytes
    }

    payload = {
        "api_key": API_KEY,
        "api_secret": API_SECRET
    }

    st.info("Comparando... Aguarde.")

    response = requests.post(COMPARE_URL, data=payload, files=files)
    result = response.json()

    st.subheader("Resultado da API")
    st.write(result)

    # Verificar resposta
    if "confidence" in result and "thresholds" in result:
        confidence = result["confidence"]
        threshold = result["thresholds"]["1e-3"]

        if confidence > threshold:
            st.success(f"✔ As faces são da MESMA pessoa! Confiança: {confidence:.2f}")
        else:
            st.warning(f"✘ As faces NÃO são da mesma pessoa. Confiança: {confidence:.2f}")
    else:
        st.error("Não foi possível comparar as faces. Verifique as imagens e sua API Key/Secret.")