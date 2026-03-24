import React, { useState, useRef, useEffect } from 'react';
import './DSATable.css';

const columns = [
  'S.No', 'Problem Name', 'Link',
  '1st Try (Date)', '1st_Myself', '1st_Help', '1st_Time(min)',
  '2nd Try (Date)', '2nd_Myself', '2nd_Help', '2nd_Time(min)',
  '3rd Try (Date)', '3rd_Myself', '3rd_Help', '3rd_Time(min)',
  '4th Try (Date)', '4th_Myself', '4th_Help', '4th_Time(min)',
  'Notes', 'Last Performance', 'Next Review'
];

const sampleData = [
  {
    problemName: 'Two Sum',
    link: 'https://leetcode.com/problems/two-sum/',
    tries: [
      { date: '12/1', myself: true, help: false, time: 10 },
      { date: '12/5', myself: false, help: true, time: 15 },
      {},
      {},
    ],
    notes: 'Classic hashmap problem.',
    lastPerformance: 'Good',
    nextReview: '12/12',
  },
  {
    problemName: 'Reverse Linked List',
    link: 'https://leetcode.com/problems/reverse-linked-list/',
    tries: [
      { date: '12/2', myself: true, help: false, time: 20 },
      {},
      {},
      {},
    ],
    notes: 'Remember pointer manipulation.',
    lastPerformance: 'Mid',
    nextReview: '12/9',
  },
];

const renderTry = (tryObj) => {
  return tryObj && tryObj.date ? (
    <>
      <div>{tryObj.date}</div>
      <div>{tryObj.myself ? '✔️' : ''}</div>
      <div>{tryObj.help ? '✔️' : ''}</div>
      <div>{tryObj.time ? `${tryObj.time}m` : ''}</div>
    </>
  ) : (
    <span>-</span>
  );
};

const DSATable = () => {
  const [zoom, setZoom] = useState(1);
  const tableWrapperRef = useRef(null);

  useEffect(() => {
    const handleWheel = (e) => {
      if ((e.ctrlKey || e.metaKey) && tableWrapperRef.current && tableWrapperRef.current.contains(e.target)) {
        e.preventDefault();
        setZoom(z => {
          let next = z - e.deltaY * 0.001;
          next = Math.max(0.5, Math.min(2, next));
          return next;
        });
      }
    };
    window.addEventListener('wheel', handleWheel, { passive: false });
    return () => window.removeEventListener('wheel', handleWheel);
  }, []);

  return (
    <div className="dsa-table-container" ref={tableWrapperRef}>
      <div style={{ overflowX: 'auto', width: '100vw', margin: 0, padding: 0 }}>
        <div style={{ transform: `scale(${zoom})`, transformOrigin: 'left top', transition: 'transform 0.2s', width: '100vw' }}>
          <table className="dsa-table">
            <thead>
              <tr>
                {columns.map((col, idx) => (
                  <th key={idx}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sampleData.map((problem, idx) => (
                <tr key={idx}>
                  <td>{idx + 1}</td>
                  <td>{problem.problemName}</td>
                  <td>
                    <a href={problem.link} target="_blank" rel="noopener noreferrer" style={{ color: '#61dafb' }}>
                      Link
                    </a>
                  </td>
                  {/* 1st to 4th Try columns */}
                  {Array.from({ length: 4 }).map((_, tryIdx) => (
                    <React.Fragment key={tryIdx}>
                      <td>{problem.tries[tryIdx]?.date || '-'}</td>
                      <td>{problem.tries[tryIdx]?.myself ? '✔️' : ''}</td>
                      <td>{problem.tries[tryIdx]?.help ? '✔️' : ''}</td>
                      <td>{problem.tries[tryIdx]?.time ? `${problem.tries[tryIdx].time}m` : '-'}</td>
                    </React.Fragment>
                  ))}
                  <td style={{ minWidth: 120, whiteSpace: 'pre-line' }}>{problem.notes}</td>
                  <td>{problem.lastPerformance}</td>
                  <td>{problem.nextReview}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DSATable; 