# Use official Python 3.9 image from Docker Hub
FROM harshan1996/paddleocr:cc

# Set working directory inside the container
WORKDIR /app

# Copy everything from current directory to /app inside container
COPY . /app

# (Optional) Install requirements if you have a requirements.txt
#RUN pip install --upgrade pip

# RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install -r requirements.txt

# Expose port 5000 to allow external access
EXPOSE 5000

# Default command to run your app
CMD ["python", "app/main.py"]
