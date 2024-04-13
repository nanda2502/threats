setwd("C:/Users/Nanda/Desktop/threats/results")
figures_path <- "../figures"
showIndRuns <- 1

probabilities <- seq(0.1, 0.9, by = 0.2)
threats <- c(0,5,10,15,20,25,30)

# Ensure the figures_path exists or create it
if (!dir.exists(figures_path)) {
  dir.create(figures_path)
}

for (probability in probabilities) {
  png(filename = paste(figures_path, sprintf("/contribution_strategies_p%g.png", probability), sep = ""), width = 800, height = 600)
  
  par(mfrow = c(1,2), cex.lab = 1, cex.axis = 1, lend = 1, las = 1)
  
  x <- 0:6 * 5
  coop <- vector()
  Cs <- vector()
  Ds <- vector()
  Os <- vector()
  coopcoop <- vector()
  
  # Plot for cooperation strategies
  plot(x, x*0, type = 'n', ylim = c(0,1),
       xlab = 'Threat severity \u03C4', ylab = 'Long term average pop. proportion', 
       main = paste('Contribution Strategies (p =', probability, ')'))
  
  for (threat in threats){
    CC <- DD <- OO <- numeric()
    for (repl in 1:3){
      print(paste('Threat level:', threat, "Probability:", probability, "Replication:", repl))
      na <- paste('contProps_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0p', probability, 'repl', repl, '.0.txt', sep = '')
      a <- if(file.exists(na)) {
        read.table(na, header = TRUE, sep = ',')
      }else {
        data.frame(C=NA, D=NA, Oc=NA, Od=NA)
        print(paste("File not found: ", na))
      }
      a$O <- a$Oc + a$Od
      if(showIndRuns == 1 && nrow(a) > 0){
        points(threat - 1 + runif(1) * 2, mean(a$C),  col = 'black', pch = 24, bg = 'blue', cex = 0.5)
        points(threat - 1 + runif(1) * 2, mean(a$D),  col = 'black', pch = 25, bg = 'red', cex = 0.5)
        points(threat - 1 + runif(1) * 2, mean(a$O),  col = 'black', pch = 23, bg = 'purple', cex = 0.5)
      }
      CC <- c(CC, mean(a$C, na.rm = TRUE))
      DD <- c(DD, mean(a$D, na.rm = TRUE))
      OO <- c(OO, mean(a$O, na.rm = TRUE))
    }
    Cs <- c(Cs, mean(CC, na.rm = TRUE))
    Ds <- c(Ds, mean(DD, na.rm = TRUE))
    Os <- c(Os, mean(OO, na.rm = TRUE))
  }
  lines(x, Cs, lty = 2, col = 'blue')
  points(x, Cs, pch = 24, bg = 'blue', col = 'black')
  lines(x, Ds, lty = 2, col = 'red')
  points(x, Ds, pch = 25, bg = 'red', col = 'black')
  lines(x, Os, lty = 2, col = 'purple')
  points(x, Os, pch = 23, bg = 'purple', col = 'black')
  
  legend('topleft', c('C', 'D', 'O'), lty = c(2,2,2), 
         col = c('black'), cex = c(1,1,1),
         pch = c(24, 25, 23), pt.bg = c('blue', 'red', 'purple'))
  # Calculate and plot cooperation percentage
  for (threat in threats){
    coopcoop <- numeric() # Reset for each threat level
    for (repl in 1:3){
      na <- paste('stats_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0p', probability, 'repl', repl, '.0.txt', sep = '')
      if (file.exists(na)){
        a <- read.table(na, header = TRUE, sep = ',')
        coopperc <- mean(a$coopPerc, na.rm = TRUE) 
        coopcoop <- c(coopcoop, coopperc)
      
        if(showIndRuns == 1){
          points(threat - 1 + runif(1) * 2, coopperc, pch = 16, col = 'black', cex = 0.5)
        }
      }
    }
    coop <- c(coop, mean(coopcoop, na.rm = TRUE))
  }
  lines(x, coop, lty = 3, col = 'black')
  points(x, coop, pch = 19, col = 'black', cex = 1.5)
  
  # Add coop% legend entry
  legend('topleft', c('C', 'D', 'O', '%Coop'), lty = c(2,2,2,3), 
         col = c('black'), cex = c(1,1,1,1), 
         pch = c(24, 25, 23, 19), pt.bg = c('blue', 'red', 'purple', NA))
  # This prepares for the punishment strategies plot
  Rs <- As <- Ss <- Ns <- numeric()
  Rs <- As <- Ss <- Ns <- numeric()
  # Plot for punishment strategies
  plot(x, x*0, type = 'n', ylim = c(0,1), 
       xlab = 'Threat severity \u03C4', ylab = '', main = paste('Punishment Strategies (p =', probability, ')'))
  
  for (threat in threats){
    RR <- AA <- SS <- NN <- numeric()
    for (repl in 1:3){
      na <- paste('punProps_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0p', probability, 'repl', repl, '.0.txt', sep = '')
      a <- read.table(na, header = TRUE, sep = ',') 
      
      if(showIndRuns == 1 && nrow(a) > 0){
        points(threat - 1 + runif(1) * 2, mean(a$R), bg = 'forestgreen', pch = 24, col = 'black', cex = 0.5)
        points(threat - 1 + runif(1) * 2, mean(a$N), bg = 'deepskyblue', pch = 22, col = 'black', cex = 0.5)
        points(threat - 1 + runif(1) * 2, mean(a$A), bg = 'darkorange', pch = 23, col = 'black', cex = 0.5)
        points(threat - 1 + runif(1) * 2, mean(a$S), bg = 'violet', pch = 25, col = 'black', cex = 0.5)
      }
      RR <- c(RR, mean(a$R, na.rm = TRUE))
      AA <- c(AA, mean(a$A, na.rm = TRUE))
      SS <- c(SS, mean(a$S, na.rm = TRUE))
      NN <- c(NN, mean(a$N, na.rm = TRUE))
    }
    Rs <- c(Rs, mean(RR, na.rm = TRUE))
    As <- c(As, mean(AA, na.rm = TRUE))
    Ss <- c(Ss, mean(SS, na.rm = TRUE))
    Ns <- c(Ns, mean(NN, na.rm = TRUE))
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
}

plots <- list()

for (i in 1:length(probabilities)){
  probability <- probabilities[i]
  plots[[i]] <- magick::image_read(paste('../figures/contribution_strategies_p', probability, '.png', sep = ''))
}

row1 <- magick::image_append(c(plots[[1]], plots[[2]], plots[[3]]))
row2 <- magick::image_append(c(plots[[4]],plots[[5]]))

final_plot <- magick::image_append(c(row1, row2),stack = T)

x_pos <- 5
y_pos <- 5
x_increment <- 800 
y_increment <- 600 

# Annotating letters a-e with a loop
letters <- c("a", "b", "c", "d", "e")
for (i in 1:length(probabilities)) {
  # Calculate position
  posX <- x_pos + ((i - 1) %% 3) * x_increment
  posY <- y_pos + ((i - 1) %/% 3) * y_increment
  
  location_str <- paste0("+", posX, "+", posY)
  
  final_plot <- magick::image_annotate(final_plot, letters[i], location = location_str, size = 50, color = "black")
}
magick::image_write(final_plot, "../figures/composite_plot.png")

