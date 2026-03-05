"""
AI Math Tutor - Main Streamlit Application
A complete system for solving algebra equations from handwritten/printed images.
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Import services and utilities
from services.ocr_service import OCRService
from services.equation_parser import EquationParser
from services.solver_service import SolverService
from services.step_generator import StepGenerator
from services.mistake_detector import MistakeDetector
from utils.image_preprocess import preprocess_image, get_image_stats
from utils.latex_converter import simple_to_latex, equation_to_latex
from utils.logger import logger, log_error


# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="AI Math Tutor",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
    }
    .equation-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #ffcccc;
        padding: 15px;
        border-radius: 8px;
        color: #cc0000;
    }
    .success-box {
        background-color: #ccffcc;
        padding: 15px;
        border-radius: 8px;
        color: #00cc00;
    }
    .warning-box {
        background-color: #ffffcc;
        padding: 15px;
        border-radius: 8px;
        color: #ff9900;
    }
    </style>
""", unsafe_allow_html=True)


# ==================== SIDEBAR CONFIGURATION ====================

with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("---")
    
    # Information
    st.markdown("""
    ### About AI Math Tutor
    
    This tool helps students learn algebra by:
    1. 🖼️ Uploading equation images
    2. 🔍 Using OCR to extract equations
    3. 📊 Solving equations step-by-step
    4. ⚠️ Detecting common mistakes
    5. 💡 Explaining solutions
    
    **Supported Equation Types:**
    - Linear equations (ax + b = c)
    - Quadratic equations (ax² + bx + c = 0)
    - Polynomial equations
    """)
    
    st.markdown("---")
    
    # Settings
    st.subheader("Settings")
    ocr_confidence_threshold = st.slider(
        "OCR Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05,
        help="Minimum confidence for OCR results"
    )
    
    show_image_stats = st.checkbox("Show Image Statistics", value=False)
    show_latex = st.checkbox("Show LaTeX Code", value=False)


# ==================== MAIN CONTENT ====================

st.title("📐 AI Math Tutor")
st.markdown("**Learn algebra step-by-step with AI assistance**")
st.markdown("---")

# Create two columns for upload and display
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📸 Upload Equation Image")
    
    uploaded_file = st.file_uploader(
        "Choose an image with an algebra equation",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG, PNG. Max size: 200MB"
    )

with col2:
    st.subheader("👁️ Image Preview")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True, caption="Uploaded image")


# ==================== PROCESSING SECTION ====================

if uploaded_file is not None:
    st.markdown("---")
    st.subheader("🔍 Processing Steps")
    
    # Convert uploaded image to OpenCV format
    image_array = np.array(Image.open(uploaded_file))
    if len(image_array.shape) == 3 and image_array.shape[2] == 4:  # RGBA
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)
    elif len(image_array.shape) == 3 and image_array.shape[2] == 3:  # RGB
        image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # Step 1: Preprocess Image
    with st.spinner("🖼️ Preprocessing image..."):
        preprocessed_image, prep_success = preprocess_image(image_array)
        
        if prep_success:
            st.success("✅ Image preprocessed successfully")
            
            if show_image_stats:
                stats = get_image_stats(preprocessed_image)
                with st.expander("📊 Image Statistics"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Height", stats.get("height", "N/A"))
                    col2.metric("Width", stats.get("width", "N/A"))
                    col3.metric("Mean Intensity", f"{stats.get('mean_intensity', 0):.2f}")
        else:
            st.error("❌ Failed to preprocess image")
            st.stop()
    
    # Step 2: Extract Text with OCR
    with st.spinner("🔍 Recognizing equation with OCR..."):
        ocr_service = OCRService()
        extracted_text, confidence, ocr_success = ocr_service.process_image(preprocessed_image)
        
        if ocr_success and confidence >= ocr_confidence_threshold:
            st.success(f"✅ OCR successful (Confidence: {confidence:.2%})")
        else:
            st.warning(f"⚠️ OCR confidence low ({confidence:.2%}). Results may be inaccurate.")
    
    # Display recognized equation
    st.subheader("📝 Recognized Equation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Allow user to edit the equation
        equation_text = st.text_input(
            "Edit equation if needed:",
            value=extracted_text,
            help="You can manually correct the equation if OCR made mistakes"
        )
    
    with col2:
        clear_button = st.button("🔄 Clear", key="clear_equation")
        if clear_button:
            st.rerun()
    
    if equation_text:
        # Show LaTeX preview
        latex_preview = simple_to_latex(equation_text)
        st.markdown(f"**LaTeX Preview:** ${latex_preview}$")
        
        if show_latex:
            st.code(latex_preview, language="latex")
    
    # ==================== SOLVING SECTION ====================
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        parse_button = st.button("🔗 Parse Equation", key="parse_button", use_container_width=True)
    
    with col2:
        solve_button = st.button("✨ Solve Equation", key="solve_button", use_container_width=True)
    
    st.markdown("---")
    
    if parse_button or solve_button:
        # Parse equation
        with st.spinner("⏳ Parsing equation..."):
            parser = EquationParser()
            equation_obj, parse_success, parse_msg = parser.parse_equation(equation_text)
            
            if not parse_success:
                st.error(f"❌ Parse Error: {parse_msg}")
                st.stop()
            else:
                st.success("✅ Equation parsed successfully")
        
        # Display parsed equation
        st.subheader("✅ Parsed Equation")
        st.write(f"**Equation:** {equation_obj}")
        
        # Detect mistakes
        with st.spinner("🔎 Detecting common mistakes..."):
            mistake_detector = MistakeDetector()
            mistakes = mistake_detector.detect_mistakes(equation_text)
            trap_areas = mistake_detector.get_trap_areas(equation_text)
            
            if mistakes:
                st.subheader("⚠️ Potential Issues Detected")
                for mistake in mistakes:
                    if mistake["severity"] == "critical":
                        st.error(f"🔴 **{mistake['type'].upper()}**: {mistake['description']}")
                    elif mistake["severity"] == "high":
                        st.warning(f"🟠 **{mistake['type'].upper()}**: {mistake['description']}")
                    else:
                        st.info(f"🟡 **{mistake['type'].upper()}**: {mistake['description']}")
            
            if trap_areas:
                st.subheader("💡 Common Trap Areas for This Equation")
                for i, trap in enumerate(trap_areas, 1):
                    st.info(f"**{i}.** {trap}")
        
        # Solve if button was pressed
        if solve_button:
            with st.spinner("📊 Solving equation..."):
                solver = SolverService()
                result = solver.solve_and_simplify(equation_obj)
                
                if result["success"]:
                    st.success("✅ Equation solved successfully")
                    
                    # Display solution
                    st.subheader("🏆 Solution")
                    
                    if result["solutions"]:
                        solution_str = ", ".join(result["solutions"])
                        st.markdown(f"## x = {solution_str}")
                        
                        # Display equation type
                        eq_type = solver.get_equation_type(equation_obj)
                        st.info(f"**Equation Type:** {eq_type.title()}")
                    else:
                        st.warning("⚠️ No solutions found (may be infinite or no solutions)")
                else:
                    st.error(f"❌ Solver Error: {result['message']}")
                    st.stop()
            
            # Generate step-by-step solution
            with st.spinner("📚 Generating step-by-step solution..."):
                step_generator = StepGenerator()
                solution_steps = step_generator.generate_complete_solution(
                    equation_obj,
                    result["solutions"]
                )
                
                if solution_steps["success"]:
                    st.subheader("📖 Step-by-Step Solution")
                    
                    if solution_steps["has_gemini"]:
                        st.info("✨ Using AI-powered explanations (Gemini)")
                    
                    # Display each step
                    for step in solution_steps["steps"]:
                        with st.expander(
                            f"Step {step.get('step_number', '?')}: {step.get('title', 'Step')}",
                            expanded=(step.get('step_number') == 1)
                        ):
                            st.write(f"**Description:** {step.get('description', 'N/A')}")
                            st.markdown(f"**Equation:** {step.get('equation', 'N/A')}")
                else:
                    st.warning("⚠️ Could not generate detailed steps")
            
            # Final summary
            st.markdown("---")
            st.subheader("📊 Summary")
            
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                st.metric("Equation Type", solver.get_equation_type(equation_obj).title())
            
            with summary_col2:
                st.metric("Number of Solutions", len(result.get("solutions", [])))
            
            with summary_col3:
                if mistakes:
                    st.metric("Issues Found", len(mistakes))
                else:
                    st.metric("Issues Found", 0)


else:
    st.info(
        """
        👈 **Start by uploading an image** with a math equation!
        
        **How to use:**
        1. Upload an image (JPG, PNG) containing an algebra equation
        2. Review the OCR result and correct if needed
        3. Click "Parse Equation" to validate the syntax
        4. Click "Solve Equation" to get step-by-step solution
        5. View detailed explanations and common pitfalls
        
        **Works with:**
        - Linear equations: 2x + 5 = 15
        - Quadratic equations: x² - 5x + 6 = 0
        - Polynomial equations: x³ - 2x² + x = 0
        """
    )


# ==================== FOOTER ====================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
    <p><strong>AI Math Tutor v1.0</strong></p>
    <p>Powered by Streamlit, SymPy, EasyOCR, and Google Gemini</p>
    <p>Learn algebra, solve problems, avoid common mistakes</p>
    </div>
    """,
    unsafe_allow_html=True
)
