import pandas as pd;
from bs4 import BeautifulSoup
from transformers import pipeline

dataset = pd.read_csv('./dataset/clubeceticismo_dataset.csv', sep=',', encoding = "utf-8", usecols=[0,1,2,3,4,5,6,7,8,9], names=["Topic ID", "Post ID", "Topic Name", "Forum Name", "Topic Link", "Username", "User Link", "User Total Messages", "Post Date Time", "Post Content"])
print(dataset.head())

def normalizeHTMLtoText(snnipedHTML):
  # Crie um objeto BeautifulSoup passando o snippet HTML e o analisador desejado (no caso, 'html.parser')
  soup = BeautifulSoup(snnipedHTML, 'html.parser')

  # Encontre todas as tags 'blockquote' e remova-as
  for blockquote in soup.find_all('blockquote'):
      blockquote.extract()

  # Imprima o texto do html sem o conteúdo das tags blockquote
  return soup.get_text()

normalizedPostContent = dataset['Post Content'].apply(normalizeHTMLtoText).to_numpy().tolist()

nlp = pipeline(model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", top_k=None, truncation=True)

def measureToxicity(texto):
    results = nlp(texto)
    return results


def formatToxicity(toxicity_array):
    formatted_results = []

    for toxicity in toxicity_array:
        label_toxicity = max(toxicity, key=lambda x: x['score'])['label']
        formatted_result = {
            'toxicity': label_toxicity,
            'positive': None,
            'negative': None,
            'neutral': None
        }

        for item in toxicity:
            label = item['label']
            score = item['score']
            formatted_result[label] = score
        formatted_results.append(formatted_result)
    return formatted_results

def salvar_csv(array_objetos, nome_arquivo):
    dataframe = pd.DataFrame(array_objetos)
    dataframe.to_csv(nome_arquivo, index=False)  # O argumento index=False evita que o Pandas inclua os índices no arquivo CSV


toxicity = measureToxicity(normalizedPostContent)
formatedToxicity = formatToxicity(toxicity)

salvar_csv(formatedToxicity, './result.csv')