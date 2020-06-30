import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

webpage = requests.get('https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html').content

soup = BeautifulSoup(webpage,"html.parser")

#How are ratings distributed?

ratings_data = soup.find_all(attrs={"class": "Rating"})

ratings = []
for rating in ratings_data[1:]:
  ratings.append(float(rating.string))

plt.hist(ratings)
plt.xlabel('Rating')
plt.ylabel('Number of Chocolates')
plt.title('Distribution of Choclate Ratings')
plt.show()

#Which chocolatier makes the best chocolate?

company_data = soup.select('.Company')

companies = []
for company in company_data[1:]:
  companies.append(company.string)

df = pd.DataFrame({
  'Company': companies,
  'Rating': ratings
})

average_rating = df.groupby('Company').Rating.mean()

best_ten_companies = average_rating.nlargest(10)

plt.clf()

#Is more cacao better?

cocoa_data = soup.find_all(attrs={"class": "CocoaPercent"})

cocoa_percent = []
for cocoa in cocoa_data[1:]:
  percent = int(float(cocoa.string.strip('%')))
  cocoa_percent.append(percent)

df['CocoaPercentage'] = cocoa_percent
print(df.head())

plt.scatter(df.CocoaPercentage, df.Rating)
z = np.polyfit(df.CocoaPercentage, df.Rating, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercentage, line_function(df.CocoaPercentage), "r--")
plt.show()