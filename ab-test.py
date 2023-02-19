import math
import streamlit as st
from scipy.stats import norm
from streamlit_lottie import st_lottie
import requests

def calculate_sample_size(control_cvr, min_detectable_effect, significance_level, power, daily_traffic, duration):
    """
    Calculate sample size required for an A/B test based on the desired test duration
    """
    n = None
    for i in range(duration):
        z_alpha = norm.ppf(1 - significance_level / 2)
        z_beta = norm.ppf(1 - power)
        p1 = control_cvr
        p2 = control_cvr * (1 + min_detectable_effect)
        n_i = (p1 * (1 - p1) + p2 * (1 - p2)) * ((z_alpha + z_beta) / min_detectable_effect) ** 2
        if n is None:
            n = n_i
        else:
            n += n_i
    sample_size = math.ceil(n)
    return sample_size

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


st.set_page_config(
    layout="wide"
)

st.markdown(
    """
    <style>
    body {
        background-color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def main():
    # Sidebar inputs
    with st.container():
        st.markdown("<h1 style='text-align: center; color: black;'>A/B Test Sample Size & Duration Approximator</h1>", unsafe_allow_html=True)

    with st.container():
        st.write('---')
        left_column, right_column = st.columns(2)
        
        with left_column:
            control_cvr = st.number_input("Baseline conversion rate", min_value=0.01, max_value=1.0, value=0.02, step=0.1)
            min_detectable_effect = st.number_input("Minimum detectable effect", min_value=0.0, max_value=1.0, value=0.03, step=0.01)
            significance_level = st.number_input("Significance level (Define Alpha)", min_value=0.01, max_value=1.00, value=0.05, step=0.01)
            power = st.number_input("Power", min_value=0.0, max_value=1.0, value=0.8, step=0.01)
            daily_traffic = st.number_input("Daily traffic To Page", min_value=1, value=10000, step=100)
            control_traffic_split = st.number_input("Est. Proportion To Control Traffic (%)", min_value=20, max_value=100, value=20, step=5)
            duration = st.number_input("Achieve Significance Duration (No. of Days)", min_value=1, value=14, step=1)

            # Calculate sample size based on the desired test duration
            sample_size = calculate_sample_size(control_cvr, min_detectable_effect, significance_level, power, daily_traffic, duration)
            control_traffic = sample_size * (control_traffic_split/100)
            variant_traffic = sample_size - control_traffic
            minimum_test_duration = round(math.ceil(sample_size/daily_traffic))
            results_flag = []
            if duration < 14:
                results_flag.append("Low  Confidence")
            else:
                results_flag.append("High Confidence")
            
            delta_flag = []
            if results_flag == "Low  Confidence":
                delta_flag.append(duration - 14)
            else:
                delta_flag.append(duration - 14)
            
            control_cvr = round(control_cvr,2)

        with right_column:
            lottie_hello = load_lottieurl('https://assets10.lottiefiles.com/private_files/lf30_vjfa6hkx.json')
            st_lottie(
                lottie_hello,
                speed=1,
                height = 600,
                key = 'coding'
            )
        st.write('---')    


    with st.container():
        kpi1, kpi2, kpi3, kpi7= st.columns(4)

        # create KPI 
        kpi1.metric(
            label = "Total Traffic Required",
            value = sample_size,
            help = "Total Traffic Required Based On Input Above"
        )

        kpi2.metric(

            label = "Control Traffic",
            value = round(control_traffic),
            help = "Control Traffic Based On Est. Proportion To Control"
        )

        kpi3.metric(
            label = "Variant Traffic",
            value = round(variant_traffic),
            help = "Variant Traffic Assumed For Test"
        )


        kpi7.metric(

            label = "Minimum Days For Test Duration",
            value = f" {minimum_test_duration} Days",
            help = "Minimum Number Of Days Test Live"

        )

    with st.container():
        kpi4, kpi6, kpi5, kpi7= st.columns(4)


        kpi4.metric(

            label = "Results Stregth",
            value = str(results_flag)[2:17],
            delta = f" {str(delta_flag)[1:2]} Confidence",
            help = "Likelyhood Of Achieving Results Based On Input"

        )

        kpi6.metric(

            label = "Baseline Conversion Rate",
            value = f" {control_cvr} %",

        )

        kpi5.metric(
            label = "Target Test Confidence",
            value = f" {round(100-(significance_level*100))}%",
            help = "Target Test Confidence Based On Input Above"
        )


        kpi7.metric(

            label = "Target Days To Achieve Test Confidence",
            value = f" {duration} Days",
            help = "Number Of Days to reach Target Test Confidence"

        )



if __name__ == "__main__":
    main()


