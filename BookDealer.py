#! python 3

# a script to compare book prices between Flipkart.com and Amazon.in


#imports
import bs4,re,sys,requests
from math import floor

#RegEX objects
numberRegEx = re.compile(r'(\d)+')

#setting my user-agent
headers = {
    'User-Agent': 'Argus v0.1'
}

#functions for finding isbn
def amazonISBN(link):
    req = requests.get(link, headers = headers)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    isbnEle = soup.select('td.bucket > div > ul > li:nth-of-type(4)')
    return (isbnEle[0].text[8:].strip())

def flipkartISBN(link):
    req = requests.get(link, headers = headers)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    isbnEle = soup.select('table.specTable > tr:nth-of-type(3) > td:nth-of-type(2)')
    return (isbnEle[0].text.strip())

#functions for finding prices from each website
def amazonPrice(link):
    req = requests.get(link, headers = headers)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    priceEle = soup.select('.inlineBlock-display')
    return (priceEle[0].text.strip())

def flipkartPrice(link):
    req = requests.get(link, headers = headers)
    req.raise_for_status()
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    priceEle = soup.select('.pricing > div > div > span:nth-of-type(1)')
    deliverEle = soup.select('.default-shipping-charge')
    deliveryCharge = numberRegEx.search(deliverEle[0].contents[0])
    if deliveryCharge != None:
        return ([priceEle[0].text[4:].strip(),deliveryCharge.group(0)])
    else:
        return ([priceEle[0].text[4:].strip(),0])

#functions for returing the correct link from isbn
def amazonLink(isbn):
    return('http://www.amazon.in/gp/product/'+str(isbn))
def flipkartLink(isbn):
    return('http://www.flipkart.com/search?q='+str(isbn))

#driver logic
link1=''
link2=''
if len(sys.argv) == 1:
    print ('Enter the link (Flipkart/Amazon): ')
    myLink = input().upper()
    if 'FLIPKART.COM' in myLink:
        link1 += myLink.lower()
        isbnfromlink = flipkartISBN(link1)
        link2 += amazonLink(isbnfromlink)
    elif 'AMAZON.IN' in myLink:
        link2 += myLink.lower()
        isbnfromlink = amazonISBN(link2)
        link1 += flipkartLink(isbnfromlink)
    else:
        print('\nWrong Link. Only Flipkart.com and Amazon.in Links accepted.')
        
else:
    if 'flipkart.com'.upper() in sys.argv[1].upper():
        link1 += sys.argv[1]
        isbnfromlink = flipkartISBN(link1)
        link2 += amazonLink(isbnfromlink)
    elif 'amazon.in'.upper() in sys.argv[1].upper():
        link2 += sys.argv[1]
        isbnfromlink = amazonISBN(link2)
        link1 += flipkartLink(isbnfromlink)
    else:
        print('\nWrong Link. Only Flipkart.com and Amazon.in Links accepted.')
try:
    amazonPrice = float(amazonPrice(link2))
    fkprice = flipkartPrice(link1)
    flipkartPrice = float(fkprice[0])+float(fkprice[1])
    print('\n\nAmazon Price: Rs. '+str(amazonPrice)+'\nFlipkart Price: Rs. '+str(flipkartPrice) + ' (includes shipping charges of Rs. '+ str(fkprice[1])+')')
    if amazonPrice < flipkartPrice:
        print('\nAmazon seems to be giving you a better deal. Go to:'+link2)
        price_diff = (flipkartPrice - amazonPrice)
        perc = (price_diff/amazonPrice) * 100
        print('\nThe price differnce is Rs.'+str(price_diff))
        print('\nYou can save '+str(floor(perc))+'% if you order from Amazon.in')
    else:
        print('\nFlipkart seems to be giving you a better deal. Go to:'+link1)
        price_diff = (amazonPrice - flipkartPrice)
        perc = (price_diff/flipkartPrice) * 100
        print('\nThe price differnce is Rs.'+str(price_diff))
        print('\nYou can save '+str(floor(perc))+'% if you order from Flipkart')
except:
    print('\n\n***Error While Parsing. Quitting.***')



#Test Code

#testLinkAMAZON = 'http://www.amazon.in/To-Kill-Mockingbird-Harper-Lee/dp/0099549484'
#testLinkFK = 'http://www.flipkart.com/to-kill-a-mockingbird/p/itme9xt9qzedkusb?pid=9780099549482'
#print(amazonISBN(testLinkAMAZON))
#print(flipkartISBN(testLinkFK))
#print(amazonPrice(testLinkAMAZON))
#print(flipkartPrice(testLinkFK))



#TODOs

#check for arguments, should be either a Flipkart Book link or an Amazon Book link

#find the isbn-10 info, store it globally
#flipkart:#fk-mainbody-id > div > div:nth-child(17) > div.gd-col.gu12 > div.productSpecs.specSection > table:nth-child(2) > tbody > tr:nth-child(3) > td.specsValue
#amazon:#detail_bullets_id > table > tbody > tr > td > div > ul > li:nth-child(4)

#search the book on both websites
#flipkart: http://www.flipkart.com/search?q=<isbn-10 code>
#amazon:http://www.amazon.in/gp/product/<isbn-10 code>

#find price info (include delivery charges if present, //try for fk app price too)
#flipkart:#fk-mainbody-id > div > div:nth-child(7) > div > div.right-col-wrap.lastUnit > div > div > div.shop-section-wrap > div > div.section-wrap.line.section > div.left-section-wrap.size2of5.unit > div > div.price-wrap > div > div.prices > div > span.selling-price.omniture-field
#fk (delivery):#fk-mainbody-id > div > div:nth-child(7) > div > div.right-col-wrap.lastUnit > div > div > div.shop-section-wrap > div > div.section-wrap.line.section > div.left-section-wrap.size2of5.unit > div > div.price-wrap > div > div.default-shipping-charge
#fk (app):#fk-mainbody-id > div > div:nth-child(7) > div > div.right-col-wrap.lastUnit > div > div > div.shop-section-wrap > div > div.section-wrap.line.section > div.right-section-wrap.size3of5.unit > div > div:nth-child(2) > div > div.offers-header.line > span
#amazon:#soldByThirdParty > span
#amazon (delivery):#buyNewInner > div.a-section.a-spacing-small.a-spacing-top-micro > div > span.a-color-base.buyboxShippingLabel > a

#display price and savings from original link
