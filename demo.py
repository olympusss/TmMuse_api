translation = {}

translation[ord("a")] = "а"
translation[ord("r")] = "р"
translation[ord("s")] = "с"
translation[ord("l")] = "л"
translation[ord("n")] = "н"

s1 = "арслан"
s2 = s1.translate(translation)
print(s2)
