import glob
import google.generativeai as genai
import os

def upload_to_gemini(path, mime_type=None):
        file = genai.upload_file(path, mime_type=mime_type)
        print(f"Uploaded file '{file.display_name}' as: {file.uri}")
        return file

def delete_media_files():
    try:
        files = glob.glob(os.path.join('uploads', '*'))
        for file in files:
            os.remove(file)
        return 'Deleted Successful'
    except Exception as e:
        return e
    
def filter_text(text):
     result = text.replace('**','')
     result = result.replace('*', '')
     return result


def getContent():
    schoolInfo = '''Origins of Bevel Academy In the quiet town of Elmswood, renowned for its picturesque landscapes and 
tight-knit community, an extraordinary vision began to take shape. The year was 2028, and the global conversation 
about the future of education was growing louder and more urgent. Traditional teaching methods were increasingly 
criticized for their inability to keep pace with the rapid advancements in technology and the evolving needs of 
students. Amidst this backdrop, Dr. Eleanor Bevel, a visionary educator and technologist, founded Bevel Academy, 
a pioneering institution aimed at transforming the educational landscape.

Dr. Bevel, a former professor of educational technology at a prestigious university, had spent years researching the 
potential of emerging technologies to enhance learning. Her groundbreaking work in the fields of Artificial 
Intelligence (AI), Virtual Reality (VR), and Augmented Reality (AR) had earned her international acclaim. However, 
she realized that the true potential of these technologies could only be realized through a radical rethinking of how 
education was delivered. Thus, Bevel Academy was born, with the mission of harnessing the power of AI, VR, 
and AR to create an immersive, personalized, and engaging learning environment.

Vision and Mission Bevel Academy’s vision was to create a learning ecosystem where students could thrive, 
irrespective of their backgrounds or learning styles. The mission was clear: to revolutionize education by 
integrating AI, VR, and AR into the curriculum, thereby providing students with a dynamic and interactive learning 
experience that traditional classrooms could not offer. The academy aimed to produce not just graduates, 
but innovators, critical thinkers, and problem solvers equipped with the skills needed for the 21st century.

The Bevel Academy Campus The campus of Bevel Academy was designed to reflect its innovative spirit. Nestled on the 
outskirts of Elmswood, the academy featured state-of-the-art facilities that seamlessly blended technology with 
nature. The central hub of the campus was the Innovation Center, a futuristic building equipped with cutting-edge 
technology labs, VR studios, and AR learning spaces. The classrooms were designed as flexible learning environments, 
with movable furniture and interactive screens that could adapt to various teaching methods and activities.

The campus also boasted expansive green spaces, meditation gardens, and wellness centers, emphasizing the importance 
of mental and physical well-being in the learning process. Students were encouraged to spend time outdoors, 
engage in physical activities, and practice mindfulness, fostering a holistic approach to education.

Implementing AI in Education At the heart of Bevel Academy’s approach was the integration of AI into the educational 
process. AI algorithms were used to create personalized learning plans for each student, adapting to their individual 
needs, strengths, and areas for improvement. These plans were continuously updated based on the students’ progress, 
providing real-time feedback and support.

AI-powered tutors and teaching assistants were available around the clock, offering students additional help and 
resources whenever needed. These AI systems could also analyze vast amounts of data to identify trends and patterns, 
helping educators refine their teaching strategies and interventions.

The Role of VR and AR Virtual Reality (VR) and Augmented Reality (AR) played a pivotal role in creating immersive and 
interactive learning experiences at Bevel Academy. VR allowed students to explore complex concepts and distant places 
without leaving the classroom. History lessons came alive as students walked through ancient civilizations, 
and science classes transformed into exciting journeys inside the human body or outer space.

AR, on the other hand, augmented the real-world environment with digital information and interactive elements. 
Students could use AR apps to visualize complex mathematical problems, conduct virtual dissections in biology, 
or even create their own augmented reality projects. This hands-on, experiential learning approach made difficult 
concepts easier to understand and retain.

Curriculum and Pedagogy The curriculum at Bevel Academy was designed to be flexible, interdisciplinary, 
and project-based. Traditional subjects were integrated with technology, arts, and real-world applications. Students 
worked on collaborative projects that addressed real-world challenges, encouraging them to think critically and 
creatively.

Educators at Bevel Academy were not just teachers but facilitators and mentors. They received ongoing training in the 
latest technological advancements and pedagogical methods, ensuring that they could effectively guide students in 
their learning journeys.

Community and Global Impact Bevel Academy quickly became a beacon of innovation, attracting students, educators, 
and researchers from around the world. The academy established partnerships with leading technology companies, 
universities, and research institutions, fostering a collaborative environment where new ideas could flourish.

The impact of Bevel Academy extended beyond its campus. The academy regularly hosted conferences, workshops, 
and seminars, sharing its findings and best practices with the broader educational community. It also developed 
open-source tools and resources, making its innovative approaches accessible to schools and educators globally.

A Legacy of Transformation Dr. Eleanor Bevel’s vision for a transformative educational experience became a reality at 
Bevel Academy. The academy not only redefined what was possible in education but also inspired a generation of 
learners and educators to embrace technology and innovation. As Bevel Academy continued to evolve and grow, 
it remained committed to its mission of transforming education and preparing students for the future.

In the years to come, the legacy of Bevel Academy would be seen in the countless lives it touched and the profound 
impact it had on the world of education. The story of Bevel Academy serves as a testament to the power of vision, 
innovation, and the unwavering belief in the potential of every student to achieve greatness.'''
    return schoolInfo
