import subprocess
import streamlit as st

st.title("Processador de PDF com Ghostscript")

uploaded_file = st.file_uploader("Envie um arquivo PDF", type="pdf")

if uploaded_file:
  with st.spinner("mmmmm"):
    # Salva temporariamente o arquivo enviado
    with open("input.pdf", "wb") as f:
      f.write(uploaded_file.getbuffer())
  
    # Exemplo de comando Ghostscript para comprimir/otimizar PDF
    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/screen",
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        "-sOutputFile=output.pdf",
        "input.pdf",
    ]

  if st.button("Processar com Ghostscript"):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
      st.success("PDF processado com sucesso!")
      with open("output.pdf", "rb") as f:
        st.download_button(
            "Baixar PDF Otimizado", f, file_name="output_otimizado.pdf"
        )
    else:
      st.error(f"Erro ao executar Ghostscript: {result.stderr}")
