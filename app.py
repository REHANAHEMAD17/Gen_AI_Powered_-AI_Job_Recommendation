import streamlit as st
from src.helper import extracted_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs


st.set_page_config(page_title= 'Job Recommender', layout= 'wide')
st.title('🔍 AI Job Recommender')
st.markdown('Upload yours resume and get job recommendations on yours skills and experience from Linkedin and Naukri Platforms')



uploaded_file= st.file_uploader('Upload your resume (PDF)', type= ['pdf'])

if uploaded_file:
    with st.spinner('Extracting the text from your resume...'):
        resume_text =extract_text_from_pdf(uploaded_file)


    with st.spinner('Summarizing the your resume...'):
        summary = ask_openai(f'Summarize this resume highlighting the skiils and educations: \n\n{resume_text}', max_tokens= 500)

    with st.spinner('Finding the skills Gaps...'):
        gaps = ask_openai(f'Analyze this resume and highlight missing skills , certifications, and experiences needed for better job opportunities: \n\n{resume_text}', max_tokens= 400)

    with st.spinner('Creating the Future Roadmap...'):
        roadmap= ask_openai(f'Based on this resume suggest me a future roadmap to improve this person careers procpect (skill to learn, certifications needed, industry exposure): \n\n{resume_text}', max_tokens= 400)



    # Display the nicely formulatted Results

    st.markdown('---')
    st.header('📑 Resume Summary')
    st.markdown(f"<div style= 'background-color: #000000; padding:15px; border-radius: 10 px; font-size: 16px;, color:white;'>{summary}</div>", unsafe_allow_html= True)

    st.markdown('---')
    st.header('🛠️ Skill Gaps & Missing Areas')
    st.markdown(f"<div style= 'background-color: #000000; padding:15px; border-radius: 10 px; font-size: 16px;, color:white;'>{gaps}</div>", unsafe_allow_html= True)

    st.markdown('---')
    st.header('🚀 Future Roadmap & Preparations Strategy')
    st.markdown(f"<div style= 'background-color: #000000; padding:15px; border-radius: 10 px; font-size: 16px;, color:white;'>{roadmap}</div>", unsafe_allow_html= True)

    st.success('✅ Analysis Completed Successfully!!')

    if st.button('🔍 Get Job Recommendations'):
        with st.spinner('Fetching the job recommendations...'):
            keywords= ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-seperated list only, no explanations.\n\nSummary : {summary}",max_tokens= 100)
            
            search_keywords_clean= keywords.replace("\n", "").strip()
        
        st.sucess(f'Extracted Job{search_keywords_clean}')

        with st.spinner('Fetching the jobs from Linkedin & Naukri Platform... '):
            linkedin_jobs= fetch_linkedin_jobs(search_keywords_clean, rows= 50)
            naukri_jobs= fetch_naukri_jobs(search_keywords_clean, rows= 50)


    st.markdown('---')
    st.header('💼 Top Linkedin Jobs')

    if linkedin_jobs:
        for job in linkedin_jobs:
            st.markdown(f"**{job.get('title')}** at * {job.get('companyName')}*")
            st.markdown(f"-  📍{job.get('locations')}")
            st.markdown(f"- 🖇️ [View Job]({job.get('link')})")
            st.markdown('---')
    else:
        st.warning('No Linkedin Jobs Founds.')


    st.markdown('---')
    st.header('💼 Top Naukri Jobs (India)')

    if naukri_jobs:
        for job in naukri_jobs:
            st.markdown(f"**{job.get('title')}** at * {job.get('companyName')}*")
            st.markdown(f"-  📍 {job.get('locations')}")
            st.markdown(f"- 🖇️ [View Job]({job.get('url')})")
            st.markdown('---')
    else:
        st.warning('NO Naukri Jobs Founds.')                                                    

    