def main(y):
    list = [6, 5, 4, 3, 2, 1, 0]
    res = 0
    ans = 0
    turns = 0
    list2 = [33.0, 27.5, 22.0, 16.5, 11.0, 5.5, 0]
    list3 = [34.0, 28.3, 22.7, 17.0, 11.3, 5.7, 0]
    for i in list:
        for x in list:
            var1 = list2[i] + list3[x]
            var2 = list2[x] + list3[i]
            if var1 > var2:
                res += 1
            if var1 == var2:
                ans += 1
            turns += 1


    print(res)
    print(ans)
    print(turns)

main(1)