from django.urls import path
from ecg.views.authenticate import (DoctorRegisterView,PatientRegisterView,DoctorLoginView,PatientLoginView)
from ecg.views.general import (PatientListView,DoctorListView)
from ecg.views.mqtt import (StartStreamingView,StopStreamingView)

urlpatterns = [
    # Authentication
    path('register/doctor/', DoctorRegisterView.as_view()),
    path('register/patient/', PatientRegisterView.as_view()),
    path('login/doctor/', DoctorLoginView.as_view()),
    path('login/patient/', PatientLoginView.as_view()),
    # Lists
    path('patients/', PatientListView.as_view()),
    path('doctors/', DoctorListView.as_view()),
    # MQTT Streaming
    path('mqtt/start/<int:doctor_id>/<int:patient_id>/', StartStreamingView.as_view()),
    path('mqtt/stop/<int:doctor_id>/<int:patient_id>/', StopStreamingView.as_view()),
]
