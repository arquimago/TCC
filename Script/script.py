import subprocess
import time
import smtplib

bases = ["breast","bupa","glass","satimage","kr-vs-kp","lettera","vehicle"]
algoritmos = ["original", "pareto_unico", "otimizacao_final"]
rodadas = 10

#bases = ["satimage"]
#algoritmos = ["original"]

inicio = time.time()
msg = "Este eh o resultado do experimento:\n"

def muda_base_de_dados(param): #param é o nome do parametro no vetor bases
	arquivo = open('parametros.txt','r')
	texto = arquivo.readlines()
	texto[0] = "@arquivo_treino:" + param + "\n"
	arquivo = open('parametros.txt', 'w')
	arquivo.writelines(texto)
	arquivo.close()
	

#main
for base in bases:
	muda_base_de_dados(base)
	msg += "-------------------------------------------------------\nBase: "
	msg += base
	msg += "\n"
	end_matriz = "saida-" + base + "/matriz_confusao.txt"
	end_tempos = "saida-" + base + "/tempos_execucao.txt"
	
	for algoritmo in algoritmos:
		msg += "\nAlgoritmo: "
		msg += algoritmo
		msg += "\n"
		arq_matriz = "resultados/Algoritmo " + algoritmo + " " + base + " matrizes.txt"
		arq_tempos = "resultados/Algoritmo " + algoritmo + " " + base + " tempos.txt"
		arq_resultados = "resultados/Algoritmo " + algoritmo + " " + base + " resultados.txt"
		arq_solucoes = "resultados/Algoritmo " + algoritmo + " " + base + " solucoes.txt"
		matrizes_confusao = []
		tempos_execucao = []
		solucoes = []
		for rodada in range(rodadas):
			subprocess.run(algoritmo)
			arquivo = open(end_matriz,'r')
			texto = arquivo.readlines()
			arquivo.close()
			matrizes_confusao.extend(texto)
			arquivo = open(end_tempos,'r')
			texto = arquivo.readlines()
			arquivo.close()
			tempos_execucao.extend(texto)
			rodada_atual = "================== Rodada " + str(rodada) + " ==============\n"
			solucoes.extend(rodada_atual)
			for i in range(0,10):
				end_solucao = "saida-" + base + "/saida"+str(i)+".txt"
				titulo = "============  solucao "+ str(i) + "============\n"
				arquivo = open(end_solucao,'r')
				texto = arquivo.readlines()
				arquivo.close()
				solucoes.extend(titulo)
				solucoes.extend(texto)
		print("\n\n\n")
		arquivo = open(arq_matriz, 'w')
		arquivo.writelines(matrizes_confusao)
		#arquivo.close()
		arquivo = open(arq_tempos, 'w')
		arquivo.writelines(tempos_execucao)
		#arquivo.close()
		aquivo = open(arq_solucoes, 'w')
		arquivo.writelines(solucoes)
		arquivo.close()
		
		#processamento matrizes Confusao
		matriz_confusao_final = [0,0,0,0]
		for i in range(len(matrizes_confusao)):
			matrizes_confusao[i] = matrizes_confusao[i].strip('\n')
		remover = ''
		while remover in matrizes_confusao:
			matrizes_confusao.remove(remover)
		for i in range(len(matrizes_confusao)):
			matriz_confusao_final[i%4]+=int(matrizes_confusao[i].split()[1])
		
		TP = matriz_confusao_final[0]
		FP = matriz_confusao_final[1]
		TN = matriz_confusao_final[2]
		FN = matriz_confusao_final[3]
		N = TP + FP + TN + FN

		texto = "Taxa de Erro (+): "
		taxa_de_erro_p  = FP/(TP+FN)
		texto += str(taxa_de_erro_p)
		texto += "\nTaxa de Erro (-): "
		taxa_de_erro_n = FN/(TN+FP)
		texto += str(taxa_de_erro_n)
		texto += "\nErro Total: "
		erro_total = (FP+FN)/N
		texto += str(erro_total)
		texto += "\nAcuracia: "
		acuracia = (TP+TN)/N
		texto += str(acuracia)
		texto += "\nRecall: "
		recall = TP/(TP+FN)
		texto += str(recall)
		texto += "\nPrecisao: "
		precisao = TP/(TP+FP)
		texto += str(precisao)
		texto += "\nEspecificidade: "
		especificidade = TN/(TN+FP)
		texto += str(especificidade)
		texto += "\n"
		msg += texto

		#processamento de tempos
		media_tempos = 0.0
		for i in range(len(tempos_execucao)):
			tempos_execucao[i] = tempos_execucao[i].strip('ms\n')
			media_tempos+=float(tempos_execucao[i])
		media_tempos = media_tempos/len(tempos_execucao)
		media = "A media eh " + str(media_tempos) + "ms"
		msg += media

		arquivo = open(arq_resultados, 'w')
		arquivo.write(texto)
		arquivo.write(media)
		arquivo.write("\nMatriz Confusao \n[TP, FP, TN, FN]\n")
		arquivo.write(str(matriz_confusao_final))
		arquivo.write("\nTotal de amostras: ")
		arquivo.write(str(N))
		arquivo.close()

		msg+="\nMatriz Confusao \n[TP, FP, TN, FN]\n"
		msg+=str(matriz_confusao_final)
		msg+="\nTotal de amostras: "
		msg+=str(N)
		msg+="\n"

fim = time.time()
tempo_total = fim-inicio
arquivo = open("resultados/tempo_total.txt", 'w')
arquivo.write(str(tempo_total))
arquivo.close()
msg += "\n-------------------------------------------------------"
msg += "\nTempo total de execucao: "
msg += str(tempo_total)
msg += "s"

arquivo = open("resultados/relatorio.txt", 'w')
arquivo.write(msg)
arquivo.close()

smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.starttls()
smtp.login('email', 'senha')

de = 'email'
para = ['outro-email']

smtp.sendmail(de, para, msg)
smtp.quit()