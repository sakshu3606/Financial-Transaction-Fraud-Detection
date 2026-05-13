{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0e37eccf-8641-4ba1-8668-a02f059a3a15",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app '__main__'\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.\n",
      " * Running on http://127.0.0.1:5000\n",
      "Press CTRL+C to quit\n",
      "127.0.0.1 - - [12/May/2026 15:23:45] \"GET / HTTP/1.1\" 200 -\n",
      "127.0.0.1 - - [12/May/2026 15:23:50] \"POST / HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, request\n",
    "import pandas as pd\n",
    "import joblib\n",
    "import numpy as np\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "preprocess_pipeline = joblib.load(\"logistic_reg_preprocess_pipeline.pkl\")\n",
    "model = joblib.load(\"logistic_reg.pkl\")\n",
    "\n",
    "@app.route(\"/\", methods=[\"GET\", \"POST\"])\n",
    "def index():\n",
    "    table_data = None\n",
    "    total_records = None\n",
    "    low_risk_count = None\n",
    "    high_risk_count = None\n",
    "    message = None\n",
    "    error = None\n",
    "\n",
    "    if request.method == \"POST\":\n",
    "        try:\n",
    "            uploaded_file = request.files.get(\"file\")\n",
    "\n",
    "            if uploaded_file is None or uploaded_file.filename == \"\":\n",
    "                error = \"No file selected. Please upload CSV or Excel file.\"\n",
    "                return render_template(\"index.html\", error=error)\n",
    "\n",
    "            filename = uploaded_file.filename.lower()\n",
    "\n",
    "            if filename.endswith(\".csv\"):\n",
    "                df = pd.read_csv(uploaded_file)\n",
    "            elif filename.endswith(\".xlsx\") or filename.endswith(\".xls\"):\n",
    "                df = pd.read_excel(uploaded_file)\n",
    "            else:\n",
    "                error = \"Invalid file format. Please upload only CSV, XLSX, or XLS file.\"\n",
    "                return render_template(\"index.html\", error=error)\n",
    "\n",
    "            original_df = df.copy()\n",
    "\n",
    "            if \"target\" in df.columns:\n",
    "                df = df.drop(columns=[\"target\"])\n",
    "\n",
    "            if \"transaction_id\" not in df.columns:\n",
    "                df[\"transaction_id\"] = range(1, len(df) + 1)\n",
    "\n",
    "            processed_data = preprocess_pipeline.transform(df)\n",
    "\n",
    "            pred_prob = model.predict(processed_data)\n",
    "            pred_class = (pred_prob > 0.5).astype(int).ravel()\n",
    "\n",
    "            original_df[\"Prediction\"] = pred_class\n",
    "            original_df[\"Result\"] = original_df[\"Prediction\"].map({\n",
    "                0: \"Low Risk / Normal\",\n",
    "                1: \"High Risk / Fraud\"\n",
    "            })\n",
    "\n",
    "            total_records = len(original_df)\n",
    "            low_risk_count = int((original_df[\"Prediction\"] == 0).sum())\n",
    "            high_risk_count = int((original_df[\"Prediction\"] == 1).sum())\n",
    "\n",
    "            table_data = original_df.to_html(\n",
    "                classes=\"table table-bordered table-striped table-hover text-center\",\n",
    "                index=False\n",
    "            )\n",
    "\n",
    "            message = \"Prediction completed successfully.\"\n",
    "\n",
    "        except Exception as e:\n",
    "            error = str(e)\n",
    "\n",
    "    return render_template(\n",
    "        \"index.html\",\n",
    "        table_data=table_data,\n",
    "        total_records=total_records,\n",
    "        low_risk_count=low_risk_count,\n",
    "        high_risk_count=high_risk_count,\n",
    "        message=message,\n",
    "        error=error\n",
    "    )\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=False, use_reloader=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c7fa2964-70f0-41ed-9aa1-5476dea972b1",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c4410e83-acf4-4684-99b6-e3729bb4dee2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
