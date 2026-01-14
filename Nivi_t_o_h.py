def toh(n,source,secondary,final):
    if n==0:
        return
    toh(n-1,source,final,secondary)
    print(f"Moving the disk {n} from {source} to {final}")
    toh(n-1,secondary,source,final)
if __name__=="__main__":
    n=3
    toh(n,"A","B","C")    