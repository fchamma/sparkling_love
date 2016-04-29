def best_rank(my_RDD, ranks = [1,2], regularization_parameter = 0.1, iterations = 10):
    training_RDD, validation_RDD = my_RDD.randomSplit([8, 2], seed=0L)
    validation_for_predict_RDD = validation_RDD.map(lambda x: (x[0], x[1]))
    
    seed = 5L
    errors = [0] * len(ranks)
    err_idx = 0

    min_error = float('inf')
    best_rank = -1
    rank_dict = {}
    for rank in ranks:
        model = ALS.train(training_RDD, rank, seed=seed, iterations=iterations,
                          lambda_=regularization_parameter)
        predictions = model.predictAll(validation_for_predict_RDD).map(lambda r: ((r[0], r[1]), r[2]))
        rates_and_preds = validation_RDD.map(lambda r: ((int(r[0]), int(r[1])), float(r[2]))).join(predictions)
        error = math.sqrt(rates_and_preds.map(lambda r: (r[1][0] - r[1][1])**2).mean())
        errors[err_idx] = error
        err_idx += 1
        print 'For rank %s the RMSE is %s' % (rank, error)
        rank_dict[rank] = error
        if error < min_error:
            min_error = error
            best_rank = rank

    print 'The best model was trained with rank %s' % best_rank

    return rank_dict