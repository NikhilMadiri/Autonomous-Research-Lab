import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, BookOpen, Edit3, Eye, LoaderCircle, Plus, Trash2 } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';

import { Modal } from '../components/ui/Modal';
import { Toast, type ToastKind } from '../components/ui/Toast';
import { literatureApi, questionsApi } from '../services/api';
import type { Literature, LiteraturePayload, LiteratureStatus } from '../types';

const currentYear = new Date().getFullYear();

const emptyForm: LiteraturePayload = {
  title: '',
  authors: '',
  year: undefined,
  journal: '',
  doi: '',
  url: '',
  abstract: '',
  notes: '',
  citation: '',
  status: 'not_reviewed',
};

function getErrorMessage(error: unknown) {
  if (typeof error === 'object' && error !== null && 'response' in error) {
    const response = error.response as { data?: { message?: string } };
    return response.data?.message || 'Something went wrong. Please try again.';
  }
  return 'Something went wrong. Please try again.';
}

interface LiteratureFormProps {
  initialValues: LiteraturePayload;
  pending: boolean;
  onCancel: () => void;
  onSubmit: (values: LiteraturePayload) => void;
}

function LiteratureForm({
  initialValues,
  pending,
  onCancel,
  onSubmit,
}: LiteratureFormProps) {
  const [values, setValues] = useState<LiteraturePayload>(initialValues);

  function updateField<K extends keyof LiteraturePayload>(
    field: K,
    value: LiteraturePayload[K],
  ) {
    setValues((current) => ({ ...current, [field]: value }));
  }

  function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit({
      ...values,
      title: values.title.trim(),
      year: values.year ? Number(values.year) : undefined,
      url: values.url || undefined,
    });
  }

  return (
    <form className="max-h-[70vh] space-y-4 overflow-y-auto pr-1" onSubmit={submit}>
      <label className="block text-sm font-semibold">
        Title *
        <input
          className="input mt-1"
          required
          maxLength={500}
          value={values.title}
          onChange={(event) => updateField('title', event.target.value)}
        />
      </label>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm font-semibold">
          Authors
          <input
            className="input mt-1"
            value={values.authors || ''}
            onChange={(event) => updateField('authors', event.target.value)}
          />
        </label>
        <label className="block text-sm font-semibold">
          Year
          <input
            className="input mt-1"
            type="number"
            min={1900}
            max={currentYear}
            value={values.year || ''}
            onChange={(event) =>
              updateField('year', event.target.value ? Number(event.target.value) : undefined)
            }
          />
        </label>
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        <label className="block text-sm font-semibold">
          Journal
          <input
            className="input mt-1"
            value={values.journal || ''}
            onChange={(event) => updateField('journal', event.target.value)}
          />
        </label>
        <label className="block text-sm font-semibold">
          Status
          <select
            className="input mt-1"
            value={values.status}
            onChange={(event) =>
              updateField('status', event.target.value as LiteratureStatus)
            }
          >
            <option value="not_reviewed">Not reviewed</option>
            <option value="reading">Reading</option>
            <option value="reviewed">Reviewed</option>
          </select>
        </label>
      </div>
      <label className="block text-sm font-semibold">
        DOI
        <input
          className="input mt-1"
          value={values.doi || ''}
          onChange={(event) => updateField('doi', event.target.value)}
        />
      </label>
      <label className="block text-sm font-semibold">
        URL
        <input
          className="input mt-1"
          type="url"
          value={values.url || ''}
          onChange={(event) => updateField('url', event.target.value)}
        />
      </label>
      <label className="block text-sm font-semibold">
        Abstract
        <textarea
          className="input mt-1 min-h-24"
          value={values.abstract || ''}
          onChange={(event) => updateField('abstract', event.target.value)}
        />
      </label>
      <label className="block text-sm font-semibold">
        Notes
        <textarea
          className="input mt-1 min-h-20"
          value={values.notes || ''}
          onChange={(event) => updateField('notes', event.target.value)}
        />
      </label>
      <label className="block text-sm font-semibold">
        Citation
        <textarea
          className="input mt-1 min-h-20"
          value={values.citation || ''}
          onChange={(event) => updateField('citation', event.target.value)}
        />
      </label>
      <div className="flex justify-end gap-3 pt-2">
        <button type="button" className="btn bg-slate-100" onClick={onCancel}>
          Cancel
        </button>
        <button disabled={pending} className="btn-primary flex items-center gap-2" type="submit">
          {pending && <LoaderCircle className="animate-spin" size={16} />}
          {pending ? 'Saving…' : 'Save literature'}
        </button>
      </div>
    </form>
  );
}

function literatureToForm(literature: Literature): LiteraturePayload {
  return {
    title: literature.title,
    authors: literature.authors || '',
    year: literature.year,
    journal: literature.journal || '',
    doi: literature.doi || '',
    url: literature.url || '',
    abstract: literature.abstract || '',
    notes: literature.notes || '',
    citation: literature.citation || '',
    status: literature.status,
  };
}

function labelForStatus(status: LiteratureStatus) {
  return status.replace('_', ' ');
}

export function QuestionDetails() {
  const { projectId = '', questionId = '' } = useParams();
  const queryClient = useQueryClient();
  const [search, setSearch] = useState('');
  const [sort, setSort] = useState('created_at');
  const [editor, setEditor] = useState<'create' | 'edit' | null>(null);
  const [editing, setEditing] = useState<Literature | null>(null);
  const [viewing, setViewing] = useState<Literature | null>(null);
  const [toast, setToast] = useState<{ kind: ToastKind; message: string } | null>(null);

  const question = useQuery({
    queryKey: ['question', questionId],
    queryFn: () => questionsApi.get(questionId).then((response) => response.data.data),
    enabled: Boolean(questionId),
  });
  const literature = useQuery({
    queryKey: ['literature', projectId, questionId, search, sort],
    queryFn: () =>
      literatureApi
        .list(projectId, questionId, { search: search || undefined, sort })
        .then((response) => response.data.data),
    enabled: Boolean(projectId && questionId),
  });

  function invalidateLiterature() {
    return queryClient.invalidateQueries({ queryKey: ['literature', projectId, questionId] });
  }

  const createMutation = useMutation({
    mutationFn: (values: LiteraturePayload) =>
      literatureApi.create(projectId, questionId, values),
    onSuccess: async () => {
      await invalidateLiterature();
      setEditor(null);
      setToast({ kind: 'success', message: 'Literature added.' });
    },
    onError: (error) => setToast({ kind: 'error', message: getErrorMessage(error) }),
  });
  const updateMutation = useMutation({
    mutationFn: ({ id, values }: { id: string; values: LiteraturePayload }) =>
      literatureApi.update(id, values),
    onSuccess: async () => {
      await invalidateLiterature();
      setEditor(null);
      setEditing(null);
      setToast({ kind: 'success', message: 'Literature updated.' });
    },
    onError: (error) => setToast({ kind: 'error', message: getErrorMessage(error) }),
  });
  const deleteMutation = useMutation({
    mutationFn: (id: string) => literatureApi.delete(id),
    onSuccess: async () => {
      await invalidateLiterature();
      setToast({ kind: 'success', message: 'Literature deleted.' });
    },
    onError: (error) => setToast({ kind: 'error', message: getErrorMessage(error) }),
  });

  function deleteLiterature(literatureId: string) {
    if (window.confirm('Delete this literature record?')) {
      deleteMutation.mutate(literatureId);
    }
  }

  if (question.isLoading) {
    return <div className="card">Loading question…</div>;
  }
  if (question.isError || !question.data) {
    return <div className="card">Question not found.</div>;
  }

  return (
    <div>
      <Link
        to={`/projects/${projectId}`}
        className="mb-5 inline-flex items-center gap-2 text-sm font-semibold text-blue-600"
      >
        <ArrowLeft size={16} /> Back to project
      </Link>
      <div className="card mb-8 flex flex-wrap items-start justify-between gap-4">
        <div>
          <span className="text-xs font-semibold uppercase text-slate-400">
            {question.data.status}
          </span>
          <h1 className="mt-2 text-3xl font-bold">{question.data.title}</h1>
          {question.data.description && (
            <p className="mt-3 max-w-3xl text-slate-500">{question.data.description}</p>
          )}
        </div>
        <button
          className="btn-primary flex items-center gap-2"
          onClick={() => setEditor('create')}
        >
          <Plus size={17} /> Add literature
        </button>
      </div>

      <div className="mb-4 flex flex-col gap-3 sm:flex-row">
        <input
          className="input"
          placeholder="Search title, authors, or journal"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
        <select className="input sm:max-w-xs" value={sort} onChange={(event) => setSort(event.target.value)}>
          <option value="created_at">Newest</option>
          <option value="title">Title</option>
          <option value="year">Year</option>
        </select>
      </div>

      {literature.isLoading ? (
        <div className="card flex items-center gap-2 text-slate-500">
          <LoaderCircle className="animate-spin" size={18} /> Loading literature…
        </div>
      ) : literature.isError ? (
        <div className="card text-rose-600">Unable to load literature.</div>
      ) : !literature.data?.items.length ? (
        <div className="card py-12 text-center text-slate-500">
          <BookOpen className="mx-auto mb-3" size={28} />
          No literature records yet.
        </div>
      ) : (
        <div className="grid gap-4 lg:grid-cols-2">
          {literature.data.items.map((item) => (
            <article className="card" key={item.id}>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h2 className="font-bold">{item.title}</h2>
                  <p className="mt-2 text-sm text-slate-500">
                    {[item.authors, item.year, item.journal].filter(Boolean).join(' · ') ||
                      'Publication details not provided'}
                  </p>
                </div>
                <span className="whitespace-nowrap rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold capitalize text-blue-700">
                  {labelForStatus(item.status)}
                </span>
              </div>
              <div className="mt-5 flex flex-wrap gap-2">
                <button className="btn bg-slate-100" onClick={() => setViewing(item)}>
                  <Eye className="mr-1 inline" size={15} /> View
                </button>
                <button
                  className="btn bg-slate-100"
                  onClick={() => {
                    setEditing(item);
                    setEditor('edit');
                  }}
                >
                  <Edit3 className="mr-1 inline" size={15} /> Edit
                </button>
                <button
                  className="btn bg-rose-50 text-rose-700"
                  onClick={() => deleteLiterature(item.id)}
                  disabled={deleteMutation.isPending}
                >
                  <Trash2 className="mr-1 inline" size={15} /> Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      )}

      <Modal
        open={editor === 'create'}
        onClose={() => setEditor(null)}
        title="Add literature"
      >
        <LiteratureForm
          initialValues={emptyForm}
          pending={createMutation.isPending}
          onCancel={() => setEditor(null)}
          onSubmit={(values) => createMutation.mutate(values)}
        />
      </Modal>
      <Modal
        open={editor === 'edit' && Boolean(editing)}
        onClose={() => {
          setEditor(null);
          setEditing(null);
        }}
        title="Edit literature"
      >
        {editing && (
          <LiteratureForm
            initialValues={literatureToForm(editing)}
            pending={updateMutation.isPending}
            onCancel={() => {
              setEditor(null);
              setEditing(null);
            }}
            onSubmit={(values) => updateMutation.mutate({ id: editing.id, values })}
          />
        )}
      </Modal>
      <Modal open={Boolean(viewing)} onClose={() => setViewing(null)} title="Literature details">
        {viewing && (
          <div className="space-y-4 text-sm">
            <h2 className="text-xl font-bold">{viewing.title}</h2>
            {[
              ['Authors', viewing.authors],
              ['Year', viewing.year],
              ['Journal', viewing.journal],
              ['DOI', viewing.doi],
              ['URL', viewing.url],
              ['Abstract', viewing.abstract],
              ['Notes', viewing.notes],
              ['Citation', viewing.citation],
            ].map(([label, value]) =>
              value ? (
                <div key={label}>
                  <p className="font-semibold text-slate-500">{label}</p>
                  <p className="mt-1 whitespace-pre-wrap">{value}</p>
                </div>
              ) : null,
            )}
          </div>
        )}
      </Modal>
      {toast && (
        <Toast kind={toast.kind} message={toast.message} onClose={() => setToast(null)} />
      )}
    </div>
  );
}
