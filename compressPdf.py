import os
import random
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
    options = ["screen", "ebook", "printer", "prepress", "default"]
    listGray = list(range(150, 1200))
    listMono = list(range(150, 1200))
    listColor = list(range(150, 1200))
    lists = [listGray, listMono, listColor]
    if st.button("Comprimir"): 
        st.spinner(text="Iniciando os procedimentos para opções de compressão...", 
                   show_time=True, width="content"):
            with open(upInput, "wb") as f:
                f.write(upLoad.getbuffer())
            for option in options: 
                #choices = [random.choice(l) for l in lists]
                choices = [150, 150, 150]
                choicesStr = "_".join([str(choice) for choice in choices])
                upOutFinal = f"{name}_compress_{option}_{choicesStr}{ext}"
                cmd = [
                          "gs",
                          "-sDEVICE=pdfwrite",
                          "-dCompatibilityLevel=1.4",
                          f"-dPDFSETTINGS=/{option}",
                          "-dDownsampleColorImages=true", 
                          "-dColorImageDownsampleType=/Bicubic", 
                          "-dEmbedAllFonts=true", 
                          "-dSubsetFonts=true", 
                          "-dMonoImageDownsampleType=/Subsample",  
                          f"-dGrayImageResolution={choices[0]}", 
                          f"-dMonoImageResolution={choices[1]}", 
                          f"-dColorImageResolution={choices[2]}", 
                          "-dNOPAUSE",
                          "-dQUIET",
                          "-dBATCH",
                          "-dSAFER",    
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
                            rateFinal = (100 - rateComp)
                            compExp = f"inicial: {upSize}kB, final: {upOutSize}kB, opção: {option}, taxa de redução: {rateComp:.2f}%, taxa final: {rateFinal:.2f}%"  
                            st.success(f"PDF processado com sucesso! {compExp}")
                else:
                    st.error(f"Erro ao executar Ghostscript: {result.stderr}")
