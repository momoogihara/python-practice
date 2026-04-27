def average(numbers):
    sum=0    
    for i in numbers:
     sum=sum+i
    return (sum / len(numbers))
print(average([10,20,30,40,50]))