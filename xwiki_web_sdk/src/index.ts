import * as WebVoiceSdk from '@mts-exolve/web-voice-sdk';

/**
* Функция для создания экземпляра SIP
* @param {sipParams} SipLogin - логин SIP в ЛК MTS Exolve sipPassword - пароль для данного SIP логина 
*/
export function createSipInstance(sipParams: { sipLogin: string, sipPassword: string }) {
  return WebVoiceSdk.createSipInstance(sipParams);
}