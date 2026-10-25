import subprocess
import streamlit as st
import os

st.title("Processador de PDF com Ghostscript")

upLoad = st.file_uploader("Envie um arquivo PDF", type="pdf")

if upLoad:
  # Salva temporariamente o arquivo enviado
  upName = upLoad.name
  name, ext = os.path.splitext(upName)
  upInput = f"{name}_input{ext}"
  upOutPut = f"{name}_output{ext}"
  with open(upInput, "wb") as f:
    f.write(upLoad.getbuffer())
  cmd = [
      "gs",
      "-sDEVICE=pdfwrite",
      "-dCompatibilityLevel=1.4",
      "-dPDFSETTINGS=/screen",
      "-dNOPAUSE",
      "-dQUIET",
      "-dBATCH",
      f"-sOutputFile={upOutPut}",
      "input.pdf",
  ]

  if st.button("Processar com Ghostscript"):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
      st.success("PDF processado com sucesso!")
      with open(upOutPut, "rb") as f:
        st.download_button(
            "Baixar PDF Otimizado", 
            f, 
            file_name="output_otimizado.pdf"
        )
    else:
      st.error(f"Erro ao executar Ghostscript: {result.stderr}")




