import os
import subprocess
import streamlit as st

st.title("Processador de PDF com Ghostscript")
upLoad = st.file_uploader("Envie um arquivo PDF", type="pdf")
if upLoad:
    upName = upLoad.name
    upSize = upLoad.size
    name, ext = os.path.splitext(upName)
    upInput = f"{name}_input{ext}"
    upOutPut = f"{name}_output{ext}"
    upOutFinal = f"{name}_compress{ext}"
    options = ["screen", "ebook", "printer", "prepress", "default"]
    with open(upInput, "wb") as f:
        f.write(upLoad.getbuffer())
        for option in options: 
            cmd = [
                  "gs",
                  "-sDEVICE=pdfwrite",
                  "-dCompatibilityLevel=1.4",
                  f"-dPDFSETTINGS=/{option}",
                  "-dGrayImageResolution=600", 
                  "-dMonoImageResolution=1200", 
                  "-dColorImageResolution=500", 
                  "-dNOPAUSE",
                  "-dQUIET",
                  "-dBATCH",
                  f"-sOutputFile={upOutPut}",
                  f"{upInput}",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                with open(upOutPut, "rb") as f:
                    if st.download_button(
                                    f"PDF Otimizado {option}", 
                                    f, 
                                    file_name=upOutFinal
                                    ):
                        upOutSize = os.path.getsize(upOutPut)
                        rateComp = (1 - upOutSize/upSize)*100
                        compExp = f"inicial: {upSize}kB, final: {upOutSize}kB, opção: {option}, taxa: {rateComp:.2f}"  
                        st.success("PDF processado com sucesso! {compExp}")
            else:
                st.error(f"Erro ao executar Ghostscript: {result.stderr}")





