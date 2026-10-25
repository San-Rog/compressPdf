import subprocess
import os
import streamlit as st

st.title("Processador de PDF com Ghostscript")
upLoad = st.file_uploader("Envie um arquivo PDF", type="pdf")

if upLoad:
    upName = upLoad.name
    upSize = upLoad.size
    name, ext = os.path.splitext(upName)
    upTemp = f"{name}_temp{ext}"
    upFinal = f"{name}_compress{ext}"
    with open(upTemp, "wb") as f:
        f.write(upLoad.getbuffer())
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
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        st.success("PDF processado com sucesso!")
        with open(upFinal, "rb") as f:
            st.download_button(
                    "Baixar PDF Otimizado", 
                    f, 
                    file_name="output_otimizado.pdf"
                    )
    else:
        st.error(f"Erro ao executar Ghostscript: {result.stderr}")



