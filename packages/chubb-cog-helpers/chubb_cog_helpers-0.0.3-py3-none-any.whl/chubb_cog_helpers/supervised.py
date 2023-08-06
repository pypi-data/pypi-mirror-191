import pandas as pd

def lift_chart(actual, predicted, percentiles):
    per_col = str(percentiles) + '-percentiles'
            
    ActPred = pd.DataFrame({"Predicted": predicted, 
                            "Actual": actual})  
    ActPred.sort_values(by = 'Predicted', ascending = False, inplace = True)
    ActPred.reset_index(drop = True, inplace = True)
    ActPred[per_col] = pd.qcut(ActPred.index, percentiles, labels = False)

    grouped = ActPred.groupby(per_col, as_index = False)
    
    liftchart = pd.DataFrame({'Measure': 'median',
                              per_col: 0,
                              'MinPred': grouped.min()['Predicted'],
                              'MaxPred': grouped.max()['Predicted'],
                              'MeanPred': grouped.mean()['Predicted'],
                              'MeanAct': grouped.mean()['Actual'],
                              'MedianPred': grouped.median()['Predicted'],
                              'MedianAct': grouped.median()['Actual'],
                              'MinAct': grouped.min()['Actual'],
                              'MaxAct': grouped.max()['Actual'],
                              'TotalRecs': grouped.count()['Actual'] 
                             })

    liftchart[per_col] = liftchart.index + 1
    liftchart = liftchart.sort_values(by = 'MinPred', ascending = False).reset_index(drop = True)
    
    liftchart['NumEvents'] = grouped.sum()['Actual']
    liftchart['HitRate'] = liftchart['NumEvents'] / liftchart['TotalRecs']
    liftchart['PctEvents'] = liftchart['NumEvents'] / liftchart['NumEvents'].sum()
    liftchart['CumEvents'] = liftchart['PctEvents'].cumsum()
    liftchart['Lift'] = liftchart['HitRate'] / liftchart['NumEvents'].sum() / liftchart['TotalRecs'].sum()

    col_order = ['Measure', per_col,'MinPred','MaxPred',
                'TotalRecs', 'NumEvents', 'HitRate', 
                'Lift', 'PctEvents', 'CumEvents']

    liftchart = liftchart[col_order].copy()
    
    return(liftchart)

def feature_importance(train_X, train_y, test_X, test_y, model, percentiles):
    importance = []
    allvars = list(test_X.columns)

    model_base = model.fit(train_X, train_y)
    base_scores = model_base.predict_proba(test_X)[:, 1]
    base_lift = lift_chart(test_y, base_scores, percentiles)['Lift'][0] 
        
    for i in allvars:     
        train_trunc = train_X.drop(i, axis=1)
        test_trunc = test_X.drop(i, axis = 1)
        
        model2 = model.fit(train_trunc, train_y)  
        scores = model2.predict_proba(test_trunc)[:, 1]
        new_lift = lift_chart(test_y, scores, percentiles)['Lift'][0]
        
        importance.append([i , (new_lift - base_lift)]) 
        
    importance = pd.DataFrame(importance, columns = ['Variable_Removed', 'LiftChg'])
    
    model.fit(train_X, train_y)
        
    importance['Neg'] = -importance['LiftChg']
    importance['Importance'] = (importance['Neg'] - importance['Neg'].min()
                             ) / (importance['Neg'].max() - importance['Neg'].min())
    importance = importance.drop(columns = ['Neg'])
    
    return importance.sort_values(by = 'LiftChg').reset_index(drop = True)