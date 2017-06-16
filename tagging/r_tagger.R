#install.packages(c("rjson","dplyr","NLP","openNLP"))
options(java.parameters = "- Xmx1024m")
library(rjson)
library(dplyr)
library(NLP)
library(openNLP)
directory <- "~/GitHub/ABSA-Tensorflow"
dir.create(directory, recursive = TRUE, showWarnings = FALSE)
setwd(directory)

json_data <- fromJSON(file= "data/posts_preprocessed.json")
data_frame <- bind_rows(json_data)

tagPOS <-  function(x, ...) {
  s <- as.String(x)
  word_token_annotator <- Maxent_Word_Token_Annotator()
  a2 <- Annotation(1L, "sentence", 1L, nchar(s))
  a2 <- annotate(s, word_token_annotator, a2)
  a3 <- annotate(s, Maxent_POS_Tag_Annotator(), a2)
  a3w <- a3[a3$type == "word"]
  POStags <- unlist(lapply(a3w$features, `[[`, "POS"))
  POStagged <- paste(sprintf("%s/%s", s[a3w], POStags), collapse = " ")
  list(POStagged = POStagged, POStags = POStags)}

data_frame[,"pos_tagged"] <- NA

for (i in 1:nrow(data_frame)){
  data_frame$pos_tagged[i] <- tagPOS(data_frame$post_message[i])$POStagged
}

data_frame$pos_tagged[5]

