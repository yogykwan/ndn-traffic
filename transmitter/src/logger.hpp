#ifndef NTG_LOGGER_HPP
#define NTG_LOGGER_HPP

#include <cstdlib>
#include <fstream>
#include <string>

#include <boost/filesystem.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>

namespace ndn {

class Logger
{
public:
  Logger(const std::string& module)
    : m_module(module)
  {
  }

  void
  shutdownLogger()
  {
    if (m_logFile.is_open())
      {
        log("Terminating Logging Operations");
        m_logFile.close();
      }
  }

  static std::string
  getTimestamp()
  {
    boost::posix_time::ptime now;
    now = boost::posix_time::second_clock::local_time();
    return to_simple_string(now);
  }

  void
  log(const std::string& logLine)
  {
    bool printTime = true;
    bool printToConsole = true;
    if (m_logLocation.length() > 0)
      {
        if (printTime)
          m_logFile << getTimestamp() << " - ";
        m_logFile << logLine << std::endl;
        m_logFile.flush();
        if (printToConsole)
          {
            if (printTime)
              std::cout << getTimestamp() << " - ";
            std::cout << logLine << std::endl;
          }
      }
    else
      {
        if (printTime)
          std::cout << getTimestamp() << " - ";
        std::cout << logLine << std::endl;
      }
  }

  void
  initializeLog(const std::string& instanceId)
  {
    const char* envVar = std::getenv("NDN_TRAFFIC_LOGFOLDER");
    m_logLocation = "";
    if (envVar != nullptr)
      m_logLocation = envVar;

    std::string logFilename;
    if (boost::filesystem::exists(boost::filesystem::path(m_logLocation)))
      {
        if (boost::filesystem::is_directory(boost::filesystem::path(m_logLocation)))
          {
            logFilename = m_logLocation + "/" + m_module + "_" + instanceId + ".log";
            m_logFile.open(logFilename.c_str(), std::ofstream::out | std::ofstream::trunc);
            if (m_logFile.is_open())
              std::cout << "Log File Initialized: " << logFilename << std::endl;
            else
              {
                std::cout << "ERROR - Unable To Initialize A Log File At: "
                          << m_logLocation << std::endl
                          << "Using Default Output For Logging." << std::endl;
                m_logLocation = "";
              }
          }
        else
          {
            std::cout << "Environment Variable NDN_TRAFFIC_LOGFOLDER Should Be A Folder."
                      << std::endl
                      << "Using Default Output For Logging." << std::endl;
            m_logLocation = "";
          }
      }
    else
      {
        std::cout << "Environment Variable NDN_TRAFFIC_LOGFOLDER Not Set." << std::endl
                  << "Using Default Output For Logging." << std::endl;
        m_logLocation = "";
      }
  }

private:
  std::string m_module;
  std::string m_logLocation;
  std::ofstream m_logFile;
};

} // namespace ndn

#endif // NTG_LOGGER_HPP
