setwd('C://Users/Nanda/Desktop/threats/results')
figures_path <- "../figures"
png(filename=paste(figures_path, "/contribution_strategies.png", sep=""), width=800, height=600)
showIndRuns<-1

coop<-c()
Cs<-c()
Ds<-c()
Os<-c()
Ocs<-c()
Ods<-c()

par(mfrow=c(1,2), cex.lab=1, cex.axis=1, lend=1, las=1)

x<-0:6*5
plot(x, x*0, type='n', ylim=c(0,1),
	xlab='Threat level', ylab='Long term average pop. proportion', 
	main='Contribution Strategies')


for (threat in 0:6*5){
	## fetch cooperation levels
	
	CC<-c()
	DD<-c()
	OO<-c()
	coopcoop<-c()
	for (repl in 1:3){
		na<-paste('contProps_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t',  threat, '.0repl', repl, '.0.txt', sep='')
		a<-read.table(na, header=TRUE, sep=',')
		
		mC<-mean(a$C); mD<-mean(a$D)
		a$O<-a$Oc+a$Od; mO<-mean(a$O)
		CC<-c(CC,mC)
		DD<-c(DD,mD)
		OO<-c(OO,mO)
		if (showIndRuns==1){
		points(threat-1+runif(1)*2, mC, col='black', pch=24, bg='blue', cex=0.5)
		points(threat-1+runif(1)*2, mD, col='black', pch=25, bg='red', cex=0.5)
		points(threat-1+runif(1)*2, mO, col='black', pch=23, bg='purple', cex=0.5)
		}
	}	
	Cs<-c(Cs, mean(CC))
	Ds<-c(Ds, mean(DD))
#	a$O<-a$Oc+a$Od
	Os<-c(Os, mean(OO))	
#	Ods<-c(Ods, mean(a$Od))	
#	Ocs<-c(Ocs, mean(a$Oc))	
	
	for (repl in 1:3){
		na<-paste('stats_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t',  threat, '.0repl', repl, '.0.txt', sep='')
		a<-read.table(na, header=TRUE, sep=',')
		meanC<-mean(a$coopPerc)
		coopcoop<-c(coopcoop, meanC)
#		points(threat-1+runif(1)*2, meanC, pch=16, col='black', cex=0.5)
	}
	coop<-c(coop, mean(coopcoop))
}

lines(x, coop, lty=3, col='black')
points(x, coop, pch=16, col='black', cex=1.5)
lines(x, Cs, lty=2, col= 'blue')
points(x, Cs, pch=24, bg='blue', col='black')
lines(x, Ds, lty=2, col='red')
points(x, Ds, pch=25, bg='red', col='black')
lines(x, Os, lty=2, col='purple')
points(x, Os, pch=23, bg='purple', col='black')

#points(x, Ods, pch=16, col='black')
#points(x, Ocs, pch=17, col='green')

legend('topleft', c('C', 'D', 'O', '% coop'), lty=c(3,2,2,2), 
	col=c('black'), cex=c(1,1,1,1),
	pch=c(24, 25, 23, 16), pt.bg=c('blue', 'red', 'purple', 'black'))


#### punishment strategies

plot(x, x*0, type='n', 
	ylim=c(0,1), xlab='Threat level', ylab='', main='Punishment Strategies')

Rs<-c()
As<-c()
Ss<-c()
Ns<-c()
for (threat in 0:6*5){
	## fetch cooperation levels
	RR<-c()
	AA<-c()
	SS<-c()
	NN<-c()
	
	for (repl in 1:3){
		na<-paste('punProps_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0repl', repl, '.0.txt', sep='')
		a<-read.table(na, header=TRUE, sep=',')
		
		mR<-mean(a$R); mA<-mean(a$A); mS<-mean(a$S); mN<-mean(a$N)
		RR<-c(RR, mR)
		AA<-c(AA, mA)
		SS<-c(SS, mS)
		NN<-c(NN, mN)
		
		if (showIndRuns==1){
		  points(threat - 1 + runif(1) * 2, mean(a$R), bg = 'forestgreen', pch = 24, col = 'black', cex = 0.5)
		  points(threat - 1 + runif(1) * 2, mean(a$N), bg = 'deepskyblue', pch = 22, col = 'black', cex = 0.5)
		  points(threat - 1 + runif(1) * 2, mean(a$A), bg = 'darkorange', pch = 23, col = 'black', cex = 0.5)
		  points(threat - 1 + runif(1) * 2, mean(a$S), bg = 'violet', pch = 25, col = 'black', cex = 0.5)
		}
	}
	Rs<-c(Rs, mean(RR))
	As<-c(As, mean(AA))
	Ss<-c(Ss, mean(SS))
	Ns<-c(Ns, mean(NN))
}


lines(x, Rs, col = 'forestgreen', lty = 2)
points(x, Rs, pch = 24, bg = 'forestgreen', col = 'black')
lines(x, Ns, lty = 2, col = 'deepskyblue')
points(x, Ns, pch = 22, bg = 'deepskyblue', col = 'black')
lines(x, As, lty = 2, col = 'darkorange')
points(x, As, pch = 25, bg = 'darkorange', col = 'black')
lines(x, Ss, lty = 2, col = 'violet')
points(x, Ss, pch = 23, bg = 'violet', col = 'black')

legend('topleft', c('R', 'N', 'A', 'S'), lty = c(2,2,2,2), 
       col = c('forestgreen', 'deepskyblue', 'darkorange', 'violet'), 
       pch = c(24, 22, 23, 25), pt.bg = c('forestgreen', 'deepskyblue', 'darkorange', 'violet'))

dev.off()


