
def redo():
    main()

def main():
    print("Enter stress method l4/l7")
    i = input("l4/l7>")
    if "l4" in i.lower():
        import modules.l4
    elif "l7" in i.lower():
        import modules.l7
    else:
        redo()
main()