# financial_analysis_app/views.py
from django.shortcuts import render
from .models import FinancialAnalysisResult, probe_model_5l_profit
import json
from django.http import HttpResponse

def index(request):
    return render(request,'index.html')

def submit(request):
    print("AbhisheK uDIYA")
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        data = json.load(file)

        flags = probe_model_5l_profit(data['data'])
        financial_analysis_result = FinancialAnalysisResult.objects.create(
            total_revenue_5cr_flag=flags["flags"]['TOTAL_REVENUE_5CR_FLAG'],
            borrowing_to_revenue_flag=flags["flags"]['BORROWING_TO_REVENUE_FLAG'],
            iscr_flag=flags["flags"]['ISCR_FLAG'],
        )

        return render(request, 'result.html', {'result': financial_analysis_result})

    return render(request, 'index.html')
