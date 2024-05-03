setwd("C:/Users/Nanda/Desktop/threats/results")
figures_path <- "../figures"
showIndRuns <- 1

probabilities <- c(0.1, 0.3, 0.5, 0.7, 0.9, 1.0)
prob_strings <- c('0.1', '0.3', '0.5', '0.7', '0.9', '1.0')
threats <- c(0,5,10,15,20,25,30)

if (!dir.exists(figures_path)) {
  dir.create(figures_path)
}

for (i in seq_along(probabilities)) {
  probability <- probabilities[i]
  prob_string <- prob_strings[i]
  # Contribution strategies
  png(filename = paste(figures_path, sprintf("/contribution_strategies_p%g.png", probability), sep = ""), width = 400, height = 600)
  
  x <- 0:(length(threats) - 1) * 5
  coop <- Cs <- Ds <- Os <- coopcoop <- numeric()
  
  plot(x, x*0, type = 'n', ylim = c(0,1), xlab = 'Threat severity \u03C4', ylab = 'Long term average pop. proportion', main = paste('Contribution Strategies (p =', probability, ')'))
  
  for (threat in threats){
    CC <- DD <- OO <- numeric()
    for (repl in 1:3){
      na <- paste('contProps_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0p', prob_string, 'repl', repl, '.0.txt', sep = '')
      
      a <- if(file.exists(na)) read.table(na, header = TRUE, sep = ',') else data.frame(C=NA, D=NA, Oc=NA, Od=NA)
      
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
  
  for (threat in threats){
    coopcoop <- numeric() # Reset for each threat level
    for (repl in 1:3){
      na <- paste('stats_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0p', prob_string, 'repl', repl, '.0.txt', sep = '')
      if (file.exists(na)){
        a <- read.table(na, header = TRUE, sep = ',')
        coopperc <- mean(a$coopPerc, na.rm = TRUE) 
        coopcoop <- c(coopcoop, coopperc)
        if(showIndRuns == 1){
          points(threat - 1 + runif(1) * 2, coopperc, pch = 16, col = 'black', cex = 0.5)
        }
      }else print(paste('File not found:', na))
    }
    coop <- c(coop, mean(coopcoop, na.rm = TRUE))
  }
  lines(x, coop, lty = 3, col = 'black')
  points(x, coop, pch = 19, col = 'black', cex = 1.5)
  
  # Add coop% legend entry
  legend('topleft', c('C', 'D', 'O', '%Coop'), lty = c(2,2,2,3), 
         col = c('black'), cex = c(1,1,1,1), 
         pch = c(24, 25, 23, 19), pt.bg = c('blue', 'red', 'purple', NA))
  lines(x, Cs, lty = 2, col = 'blue')
  points(x, Cs, pch = 24, bg = 'blue', col = 'black')
  lines(x, Ds, lty = 2, col = 'red')
  points(x, Ds, pch = 25, bg = 'red', col = 'black')
  lines(x, Os, lty = 2, col = 'purple')
  points(x, Os, pch = 23, bg = 'purple', col = 'black')
  
  legend('topleft', legend = c('C', 'D', 'O'), lty = c(2, 2, 2), col = c('black'), pch = c(24, 25, 23), pt.bg = c('blue', 'red', 'purple'))
  
  dev.off()
  
  # Punishment strategies
  png(filename = paste(figures_path, sprintf("/punishment_strategies_p%g.png", probability), sep = ""), width = 400, height = 600)
  
  Rs <- As <- Ss <- Ns <- numeric()
  
  plot(x, x*0, type = 'n', ylim = c(0,1), xlab = 'Threat severity \u03C4', ylab = 'Long term average pop. proportion', main = paste('Punishment Strategies (p =', probability, ')'))
  
  for (threat in threats){
    RR <- AA <- SS <- NN <- numeric()
    for (repl in 1:3){
      na <- paste('punProps_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0p', prob_string, 'repl', repl, '.0.txt', sep = '')
      a <- if(file.exists(na)) read.table(na, header = TRUE, sep = ',') else data.frame(R=NA, A=NA, S=NA, N=NA)
      
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
  points(x, As, pch = 23, bg = 'darkorange', col = 'black')
  lines(x, Ss, lty = 2, col = 'violet')
  points(x, Ss, pch = 23, bg = 'violet', col = 'black')
  
  legend('topleft', legend = c('R', 'N', 'A', 'S'), lty = c(2,2,2,2), col = c('forestgreen', 'deepskyblue', 'darkorange', 'violet'), pch = c(24, 22, 23, 25), pt.bg = c('forestgreen', 'deepskyblue', 'darkorange', 'violet'))
  
  dev.off()
}


plots_contributions <- list()
plots_punishments <- list()

# Read contribution strategy images
for (i in 1:length(probabilities)){
  probability <- probabilities[i]
  plots_contributions[[i]] <- magick::image_read(paste('../figures/contribution_strategies_p', probability, '.png', sep = ''))
}

# Read punishment strategy images
for (i in 1:length(probabilities)){
  probability <- probabilities[i]
  plots_punishments[[i]] <- magick::image_read(paste('../figures/punishment_strategies_p', probability, '.png', sep = ''))
}

# Append images horizontally for both rows
row1 <- magick::image_append(c(plots_contributions[[1]], plots_contributions[[2]], plots_contributions[[3]], plots_contributions[[4]], plots_contributions[[5]], plots_contributions[[6]]), stack = FALSE)
row2 <- magick::image_append(c(plots_punishments[[1]], plots_punishments[[2]], plots_punishments[[3]], plots_punishments[[4]], plots_punishments[[5]], plots_punishments[[6]]), stack = FALSE)

# Stack the two rows vertically
final_plot <- magick::image_append(c(row1, row2), stack = TRUE)

x_pos <- 5
y_pos <- 5
x_increment <- 400 # Adjusted width since images are now half the width
y_increment <- 600 

# Annotating letters a-e for contribution and f-j for punishment with a loop
for (i in 1:(2 * length(probabilities) )) {
  posX <- x_pos + ((i - 1) %% length(probabilities)) * x_increment # Modulus 5 since there are 5 images per row
  posY <- y_pos + ((i - 1) %/% length(probabilities)) * y_increment # Integer division by 5 to switch between rows
  
  location_str <- paste0("+", posX, "+", posY)
  
  final_plot <- magick::image_annotate(final_plot, letters[i], location = location_str, size = 50, color = "black")
}

magick::image_write(final_plot, "../figures/composite_plot.png")


replaceLineIfNeeded <- function(filename) {
  if (!file.exists(filename)) {
    print(paste("File does not exist:", filename))
    return(FALSE)
  }
  
  data <- readLines(filename)
  
  if (length(data) < 3002) {
    return(FALSE)
  }
  
  line3002 <- strsplit(data[3002], split=",")[[1]]
  
  if (length(line3002) < 4) {
    data[3002] <- data[3001]
    writeLines(data, filename)
    print(paste("Line 3002 in file", filename, "replaced with line 3001."))
  }
}


fileTypes <- c("contProps", "punProps", "stats")

for (prob_string in prob_strings) {
  for (threat in threats) {
    for (fileType in fileTypes) {
      for (repl in 1:3) {
        filename <- paste(fileType, '_test2PG_b3.0c1.0l0.5rho1.5i1e0mu0.01death0.1im1bP30t', threat, '.0p', prob_string, 'repl', repl, '.0.txt', sep = '')
        replaceLineIfNeeded(filename)
      }
    }
  }
}