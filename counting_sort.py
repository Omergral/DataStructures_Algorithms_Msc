def counting_sort(A: list, k: int):
    print(f"\ninitial array A ------> {A}")
    counts = [0 for _ in range(k)]

    print(f"\n{'-'*60}\nbuilding counts array:\n")
    for a in A:
        counts[a-1] += 1
        print(f"{counts}  ----> +1 added to {a}")

    print(f"\n{'-' * 60}\ncumulative summing counts array:\n\nbefore change --> {counts}\n")

    for i in range(1, k):
        counts[i] += counts[i-1]
        print(f"{counts} added {counts[i-1]} to {counts[i]-counts[i-1]}")

    print(f"\n{'-' * 60}\ncreating sorted array:")
    B = [0 for _ in range(len(A))]
    for j in reversed(range(len(A))):
        print(f"\n\nB before change ---> {B}\nA ---> {A}"
              f"\ncounts before change --> {counts}")
        B[counts[A[j]-1]-1] = A[j]
        counts[A[j]-1] -= 1
        print(f"\nfor A[{j+1}] (that is {A[j]}):\nthe corresponds value in counts is {counts[A[j]-1]+1}")
        print(f"B array -------> {B} - placed {A[j]} in B[{counts[A[j]-1]+1}]")
        print(f"counts array -------> {counts} - counts[{A[j]-1}] (was {counts[A[j]-1]+1}) changed to {counts[A[j]-1]}")
        if j != 0:
            print("\n\n\t---Next---")
        else:
            print("\n\n\t---Done!---")


if __name__ == '__main__':
    counting_sort([4, 3, 3, 1, 2, 4, 2, 3], 4)
