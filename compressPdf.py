import subprocess
import streamlit as st
import os

st.title("Processador de PDF com Ghostscript")

upLoad = st.file_uploader("Envie um arquivo PDF", type="pdf")

if upLoad:
    upName = upLoad.name
    upSize = upLoad.size
    name, ext = os.path.splitext(upName)
    upInput = f"{name}_input{ext}"
    upOutPut = f"{name}_output{ext}"
    upOutFinal = f"{name}_compress{ext}"
    with open(upInput, "wb") as f:
        f.write(upLoad.getbuffer())
    cmd = [
          "gs",
          "-sDEVICE=pdfwrite",
          "-dCompatibilityLevel=1.4",
          "-dPDFSETTINGS=/screen",
          "-dGrayImageResolution=600", 
          "-dNOPAUSE",
          "-dQUIET",
          "-dBATCH",
          f"-sOutputFile={upOutPut}",
          "input.pdf",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        with open(upOutPut, "rb") as f:
            if st.download_button(
                        "Baixar PDF Otimizado", 
                        f, 
                        file_name=upOutFinal
                        ):
                sizeCompr = os.path.getsize(upOutPut)
                red = (1 - sizeCompr/upSize)*100
                redExpr = f"PDF processado com sucesso e redução de {red:.2f}%!"
                st.success(redExpr)     
                
    else:
        st.error(f"Erro ao executar Ghostscript: {result.stderr}")





