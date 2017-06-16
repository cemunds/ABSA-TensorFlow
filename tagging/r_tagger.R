#install.packages(c("rjson","dplyr","NLP","openNLP","jsonlite","stringr","dplyr"))
#also needs OpenNLPmodels.en from <http://datacube.wu.ac.at/>
#install.packages("openNLPmodels.en", repos = "http://datacube.wu.ac.at/", type = "source")
options(java.parameters = "- Xmx1024m")
library(rjson)
library(dplyr)
library(NLP)
library(openNLP)
library(jsonlite)
library(stringr)
library(dplyr)

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
sink("tagging/complete_tagged.json")
cat(jsonlite::toJSON(data_frame, pretty = TRUE))
sink()

jsonlite::toJSON(data_frame, pretty = TRUE)


word_ann <- Maxent_Word_Token_Annotator()
sent_ann <- Maxent_Sent_Token_Annotator()
person_ann <- Maxent_Entity_Annotator(kind = "person")
location_ann <- Maxent_Entity_Annotator(kind = "location")
organization_ann <- Maxent_Entity_Annotator(kind = "organization")
date_ann <- Maxent_Entity_Annotator(kind = "date")
money_ann <- Maxent_Entity_Annotator(kind = "money")


pipeline <- list(sent_ann,
                 word_ann,
                 person_ann,
                 location_ann,
                 organization_ann, date_ann, money_ann)

# Extract entities from an AnnotatedPlainTextDocument
entities <- function(doc, kind) {
  s <- doc$content
  a <- annotations(doc)[[1]]
  if(hasArg(kind)) {
    k <- sapply(a$features, `[[`, "kind")
    s[a[k == kind]]
  } else {
    s[a[a$type == "entity"]]
  }
}


namevector <-c('person','location','organization','sents', 'date', 'money')
data_frame[,"sents"] <- NULL

for (i in 1:nrow(data_frame)){
  annotations <- annotate(data_frame$post_message[i], pipeline)
  doc <- AnnotatedPlainTextDocument(data_frame$post_message[i], annotations)
  data_frame$organization[i] <- paste(entities(doc, kind = "organization"), collapse = ";")
  data_frame$location[i] <-paste(entities(doc, kind = "location"), collapse = ";")
  data_frame$person[i]<-paste(entities(doc, kind = "person"), collapse = ";")
  data_frame$date[i]<-paste(entities(doc, kind = "date"), collapse = ";")
  data_frame$money[i]<-paste(entities(doc, kind = "money"), collapse = ";")
  
  data_frame$sents[i] <- sents(doc)
  
}


