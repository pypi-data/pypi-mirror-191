def try_run(skymodelname):
    if skymodelname=="run":
        import run
        run.add(2,3)
        run.run()
    elif skymodelname=="join":
        import join
        a=join.club('web')
        a.addpeople('bob')
        a.addpeople('tom')
        a.delpeople('tom')
        
