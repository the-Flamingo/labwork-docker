import base64
from collections import OrderedDict
'''
assignment = {
        "action": "decimate",
        "data": "DhNAXo08awpOpdqm30HKnjvN66UyJkX0PlkNxYlP",
        "selectors": [
          {
            #"offset": 0,
            "stride": 1
          },
          {
            #"offset": 0,
            "stride": 2
          },
          {
            #"offset": 1,
            "stride": 2
          },
          {
            #"offset": 0,
            "stride": 3
          },
          {
            #"offset": 1,
            "stride": 3
          },
          {
            #"offset": 2,
            "stride": 3
          }
        ]
      }

assignment = {
        "action": "chi_square",
        "data": "//8A//7+Af7+/gH+/f0B/fz8Afz8+wH7+/sC+/r6Avr6+gL6+vkC+fn5Avj4+AL49/cD9/f2A/b29gP29fUE9fX0BPT08wXz8/IF8vLyBfLy8gXx8PAF8O/vBu/u7gbu7u4G7u7tBu3t7Qbt7OsG6urqBurq6Qbp6ekG6enpBujo6Afo6OcI5+fnCefn5wrl5eQK5OTkCuTj4gvi4uIL4uLhC+Hh4Qvh4OAL4N/fC9/e3Qzd3d0M3d3cDdzc3A3c3NwN3NzbDdvb2w7b2tkO2dnYDtjY2A7Y19cP19bWD9XV1Q/V1NQQ1NPTENPT0xHS0tIR0dHREtDQ0BLQ0NASzs7OE87NzRPNzc0TzMzMFMzMyxXLy8sVy8vKFcrKyhXJyckVycnJFsnIyBbIyMgWyMjIFsjIyBbHx8cXx8fHF8bGxRfFxcUXxcTEF8PDwxfDw8MYw8LCGMLCwhjBwcAYv7+/Gb+/vxm+vr4Zvr29Gb28vBq8vLsau7u6Grq5uRq5ubgauLi4G7i3txu3t7Ybtra2G7a2tRu0tLQbs7OzHLKyshyysrIcsbGwHbCwsB2vr64erq6tHq2trB6sq6seq6urHqqqqh+qqqofqampH6ioqB+oqKcfp6emH6amph+lpaUgpKSkIKOjoyCjo6IgoqKiIaKhoSGhoaEhoaCfIp+eniKenZ0inJycIpubmyObmpojmZmYI5iXlyOWlpYjlpWVI5WUlCSUk5Mkk5OTJJOSkiSSkZEkkJCQJI+PjySPjo4ljo6NJo2NjSaMjIwmjIuLJ4uLiieKioopioqKKYmJiSmIiIgqiIiIKoiHhyqHhoYrhoWFK4WFhSuEhIQshISELISDgyyDg4MtgoKCLYKCgS2BgYEtgYGBLYGBgS2AgIAugICAL4B/fy9+fnwvfHx8L3t7ey97enowenp6MXl5eTF5eXgxeHh4MXd3dzF3dnYxdnR0MXRzczFycnIxcnFxMnFxcDJvb28yb29vMm1tbTNtbW0zbGxsM2xsazRra2s0ampqNGpqajVqaWk2aWlpNmlpaTZpaGg3aGhoN2hoZzdnZ2c3ZmZmN2ZlZDdkZGM3Y2NjOGNjYjhiYmI4YWBgOWBgYDlfXl45XV1dOV1dXTlcXFw5W1tbOltaWjpZWFg6WFhXO1dXVztXV1c7V1ZWO1ZWVTtVVVQ7U1NSPFJRUTxRUFA8UFBQPE9PTzxPT048Tk5OPU5OTT1NTU09TExMPUxMTD1LS0s+SkpKPkpKSj5JSUg+SEhIP0dHRz9HRkY/RUVFP0RERD9ERERARENDQENDQ0BDQ0JAQkJCQEJCQUFBQUFBQQ==",
        "selectors": [
          {},
          {
            "offset": 0,
            "stride": 4
          },
          {
            "offset": 1,
            "stride": 4
          },
          {
            "offset": 2,
            "stride": 4
          },
          {
            "offset": 3,
            "stride": 4
          }
        ]
      }
'''
def handle_chi_square(assignment):
    action = assignment["action"]
    data = base64.b64decode(assignment["data"])
    selectors = assignment["selectors"]
    #print("")
    #print(action)
    #print(data)
    if action == "decimate":
        decimated_data = decimate(data, selectors) # Returns an Array with Bytearrays
        result = []
        for item in decimated_data:
            result.append({"decimated_data": base64.b64encode(item).decode("utf-8")})
        #print(result)
        return result
    elif action == "histogram":
        return histogram(decimate(data,selectors))
    elif action == "chi_square":
        return chi_square(histogram(decimate(data,selectors)))

def decimate(data, selectors):
    decimated_data = []
    for element in selectors:
        modified_data = []
        #print("Element in selectors:", element)
        if "stride" in element and "offset" in element:
            stride = int(element["stride"])
            offset = int(element["offset"])
            for byte in range(offset, len(data), stride):
                #print("Data[byte]", data[byte])
                modified_data.append(data[byte])
            #print("Modified with stride and offset:",modified_data)
            decimated_data.append(bytes(modified_data))
        elif "stride" in element and "offset" not in element:
            stride = int(element["stride"])
            for byte in range(0, len(data), stride):
                modified_data.append(data[byte])
            #print("Modified with stride:",modified_data)
            decimated_data.append(bytes(modified_data))
        elif "offset" in element and "stride" not in element:
            offset = int(element["offset"])
            for byte in range(offset, len(data)):
                modified_data.append(data[byte])
            #print("Modified with offset:",modified_data)
            decimated_data.append(bytes(modified_data))
        else:
            #print("Data not modified:",data)
            decimated_data.append(data)
    #print("Decimated data:", decimated_data)
    #for item in decimated_data:
        #print("Encoded item:", base64.b64encode(item).decode("utf-8"))
    return decimated_data

def histogram(decimated_data):
    result = []
    for data in decimated_data:
        #print("Handeling datablock:", data)
        bytes = {}
        for byte in data:
            #print("Handeling byte:", byte)
            if byte in bytes:
                bytes[byte] += 1
            else:
                bytes[byte] = 1
        ints = sorted(bytes.items())
        dictionary = {}
        for key, value in ints:
            #print(key, value)
            dictionary[key] = value
        result.append({"histogram": dictionary})
    #print("Result:", result)
    return result

def chi_square(histograms):
    # Calculate S and give desicion
    m = 256                 # categories, bins
    #t_i = range(1, 256)    # categories/bins have respective (histogram) counts, called t_i for i = 1...256
    #n = int                # "Samples (Bytes)"
    right_crit = 311
    left_crit = 205
    #print(histograms)
    result = []
    for histogram in histograms:
        #print(histogram)
        S = 0
        n = sum(histogram['histogram'].values())
        #print("Length:", n)

        for number in range(0, 256):
            if number not in (histogram['histogram']):
                histogram['histogram'][number] = 0

        for t_i in histogram['histogram'].values():
            #print("t_i:", t_i)
            S += (t_i - n/m)**2 
            #print("Current S:", S)
        S = round(S*(m/n))
        #print("Final S:", S)

        if (S < right_crit) and (S > left_crit):
            verdict = {
                "chi_square_statistic": S,
                "verdict": "no_result"
            }
        elif (S >= right_crit):
            verdict = {
                "chi_square_statistic": S,
                "verdict": "non_uniform"
            }
        elif (S <= left_crit):
            verdict = {
                "chi_square_statistic": S,
                "verdict": "uniform"
            }
        
        result.append(verdict)
    return result
