dic = {}
# Test Set 1
dic["1AJV"] = ["N01", "S02"]
dic["1AJX"] = ["N01", "C02"]
dic["1BV9"] = ["C1", "N2"]		# different disturbance code
dic["1D4K"] = ["N2", "C21"]
dic["1G2K"] = ["N01", "S02"]
dic["1HIV"] = ["N1", "CA2"]
dic["1HPX"] = ["N3", "C13"]		# last atom used was N01 instead N3
dic["1HTF"] = ["N1", "C7"]
dic["2UPJ"] = ["CA", "C1G"]

# Test Set 2
dic["1A9M"] = ["N2", "C18"]
dic["1AAQ"] = ["CM", "C2"]
dic["1B6L"] = ["C14", "C24"]
dic["1B6M"] = ["C5", "N2"]
dic["1BDL"] = ["C19", "C17"]
dic["1BDR"] = ["C20", "C19"]
dic["1GNM"] = ["O1", "C4"]
dic["1GNO"] = ["N2", "C17"]
dic["1HBV"] = ["C23", "N22"]
dic["1HEG"] = ["N4", "C3"]
dic["1HIH"] = ["C20", "C22"]
dic["1HPV"] = ["C6", "C14"]
dic["1HSG"] = ["C10", "C11"]
dic["1HTE"] = ["C3", "C4"]
dic["1IZH"] = ["C1", "C23"] 	# last atom used was C10 instead C1
dic["1KZK"] = ["C10", "C11"]
dic["1SBG"] = ["C19", "C20"] 	# last atom used was C10 instead C19
dic["1TCX"] = ["C19", "C20"] 	# last atom used was C10 instead C19
dic["1ZIR"] = ["C1", "C23"] 	# last atom used was C10 instead C1
dic["3AID"] = ["C1", "C13"]		# all atoms used are differents

# Test Set 3
dic["1B6J"] = ["N", "C6"]
dic["1B6P"] = ["N25", "C22"]
dic["1D4K"] = ["C21", "N2"]
dic["1D4L"] = ["N2", "C22"]
dic["1HEF"] = ["C10", "C2"]
dic["1HXW"] = ["C15", "C14"]
dic["1IZH"] = ["C5", "N2"]
dic["1JLD"] = ["N2", "C1"]
dic["1K6C"] = ["C10", "C11"]
dic["1K6P"] = ["C10", "C11"]
dic["1K6T"] = ["C10", "C11"]
dic["1K6V"] = ["C10", "C11"]
dic["1MTR"] = ["N1", "CA1"]
dic["1MUI"] = ["C23", "C24"]
dic["2BPX"] = ["C10", "C11"]
dic["5HVP"] = ["CM", "CH"]

def getAtomsByComplex( name ):
	return dic.get( name )[0], dic.get( name )[1]
